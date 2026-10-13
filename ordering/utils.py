"""Server-side cart cleaning and total calculation (never trust the browser)."""
from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings

from .models import MenuItem

MAX_ID = 2**31 - 1


def money(value):
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def clean_cart(raw):
    """Validate a {item_id: qty} mapping from the browser.

    Returns ({"<id>": qty}, [warning messages]). Invalid quantities are
    dropped/clamped and unavailable or missing menu items are removed.
    """
    warnings = []
    if not isinstance(raw, dict):
        return {}, warnings

    wanted = {}
    for key, value in raw.items():
        if isinstance(value, bool):
            continue
        try:
            pid, qty = int(key), int(value)
        except (TypeError, ValueError):
            continue
        if not (0 < pid <= MAX_ID) or qty < 1:
            continue
        if qty > settings.MAX_ITEM_QUANTITY:
            qty = settings.MAX_ITEM_QUANTITY
            warnings.append(f"Maximum {settings.MAX_ITEM_QUANTITY} per item.")
        wanted[pid] = qty

    items = MenuItem.objects.in_bulk(list(wanted))
    cart = {}
    for pid, qty in wanted.items():
        item = items.get(pid)
        if item is None:
            warnings.append("An item is no longer on the menu and was removed.")
        elif not item.is_available:
            warnings.append(f"{item.name} is currently unavailable and was removed.")
        else:
            cart[str(pid)] = qty
    return cart, list(dict.fromkeys(warnings))


def calculate(cart):
    """Return (lines, subtotal, tax, total) using current database prices."""
    items = MenuItem.objects.in_bulk([int(k) for k in cart])
    lines = []
    subtotal = Decimal("0")
    for key, qty in cart.items():
        item = items.get(int(key))
        if item is None:
            continue
        line_total = item.price * qty
        subtotal += line_total
        lines.append({"item": item, "quantity": qty, "line_total": money(line_total)})
    subtotal = money(subtotal)
    tax = money(subtotal * settings.TAX_RATE)
    return lines, subtotal, tax, subtotal + tax
