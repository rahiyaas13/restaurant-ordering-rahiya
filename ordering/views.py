import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .forms import CheckoutForm, StatusForm, TrackForm
from .models import Category, MenuItem, Order, OrderItem
from .utils import calculate, clean_cart


# ---------------------------------------------------------------- menu
@ensure_csrf_cookie
def menu(request):
    categories = Category.objects.prefetch_related(
        Prefetch("items", queryset=MenuItem.objects.order_by("name"))
    )
    return render(request, "ordering/menu.html", {"categories": categories})


# ---------------------------------------------------------------- cart
def _cart_page(request, form):
    items = MenuItem.objects.filter(is_available=True)
    menu_data = [
        {
            "id": i.pk,
            "name": i.name,
            "price": str(i.price),
            "veg": i.is_vegetarian,
            "image": i.image_url,
        }
        for i in items
    ]
    return render(request, "ordering/cart.html", {"form": form, "menu_data": menu_data})


@ensure_csrf_cookie
def cart(request):
    return _cart_page(request, CheckoutForm())


@require_POST
def cart_sync(request):
    """Validate the browser cart and store it in the Django session."""
    try:
        payload = json.loads(request.body or b"{}")
    except ValueError:
        return JsonResponse({"ok": False, "error": "Invalid JSON"}, status=400)
    raw = payload.get("cart") if isinstance(payload, dict) else None
    clean, warnings = clean_cart(raw)
    request.session["cart"] = clean
    _, subtotal, tax, total = calculate(clean)
    return JsonResponse(
        {
            "ok": True,
            "cart": clean,
            "warnings": warnings,
            "subtotal": str(subtotal),
            "tax": str(tax),
            "total": str(total),
        }
    )


@require_POST
def checkout(request):
    form = CheckoutForm(request.POST)
    cart_data, warnings = clean_cart(request.session.get("cart"))
    request.session["cart"] = cart_data
    for w in warnings:
        messages.warning(request, w)

    if not cart_data:
        messages.error(request, "Your cart is empty.")
        return redirect("cart")
    if not form.is_valid():
        return _cart_page(request, form)

    # Totals are recalculated on the server from database prices.
    lines, subtotal, tax, total = calculate(cart_data)
    with transaction.atomic():
        order = form.save(commit=False)
        order.subtotal, order.tax_amount, order.total_amount = subtotal, tax, total
        order.status = Order.RECEIVED
        order.save()
        OrderItem.objects.bulk_create(
            OrderItem(
                order=order,
                menu_item=line["item"],
                quantity=line["quantity"],
                unit_price=line["item"].price,
            )
            for line in lines
        )

    request.session.pop("cart", None)  # clear the session cart
    messages.success(request, f"Order placed! Your Order ID is #{order.pk}.")
    return redirect(f"/track/{order.pk}/?placed=1")


# ---------------------------------------------------------------- tracking
def track_lookup(request):
    form = TrackForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        order_id = form.cleaned_data["order_id"]
        if Order.objects.filter(pk=order_id).exists():
            return redirect("track_order", pk=order_id)
        form.add_error("order_id", "No order found with that ID.")
    return render(request, "ordering/track_form.html", {"form": form})


def track_order(request, pk):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__menu_item"), pk=pk
    )
    steps = [
        {"code": code, "label": label, "done": i <= order.status_index, "current": i == order.status_index}
        for i, (code, label) in enumerate(Order.STATUS_CHOICES)
    ]
    placed = request.GET.get("placed") == "1"
    return render(
        request,
        "ordering/track.html",
        {"order": order, "steps": steps, "just_placed": placed, "clear_cart": placed},
    )


# ---------------------------------------------------------------- kitchen
@staff_member_required(login_url="login")
def kitchen(request):
    orders = Order.objects.prefetch_related("items__menu_item")
    columns = []
    for code, label in Order.STATUS_CHOICES:
        qs = orders.filter(status=code)
        qs = qs.order_by("-updated_at")[:12] if code == Order.COMPLETED else qs.order_by("created_at")
        columns.append({"code": code, "label": label, "orders": list(qs)})
    return render(request, "ordering/kitchen.html", {"columns": columns})


@staff_member_required(login_url="login")
@require_POST
def kitchen_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = StatusForm(request.POST)
    if form.is_valid():
        order.status = form.cleaned_data["status"]
        order.save(update_fields=["status", "updated_at"])
        messages.success(request, f"Order #{order.pk} is now {order.get_status_display()}.")
    else:
        messages.error(request, "Invalid status.")
    return redirect("kitchen")
