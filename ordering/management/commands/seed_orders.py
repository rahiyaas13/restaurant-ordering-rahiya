from django.core.management.base import BaseCommand

from ordering.models import MenuItem, Order, OrderItem
from ordering.utils import calculate

# (customer_name, phone, table_number, notes, status, [(item_name, qty), ...])
SAMPLE_ORDERS = [
    (
        "Arjun Mehta", "9876543210", 3, "No onions please",
        Order.COMPLETED,
        [("Paneer Tikka", 1), ("Butter Chicken", 1), ("Garlic Naan", 2), ("Mango Lassi", 2)],
    ),
    (
        "Priya Sharma", "9123456780", 7, "",
        Order.READY,
        [("Hara Bhara Kebab", 2), ("Veg Dum Biryani", 1), ("Masala Chai", 2)],
    ),
    (
        "Rohit Verma", "9988776655", 1, "Extra spicy",
        Order.PREPARING,
        [("Chicken 65", 1), ("Hyderabadi Chicken Biryani", 2), ("Fresh Lime Soda", 2)],
    ),
    (
        "Sneha Iyer", "9765432100", 5, "Celebrate birthday",
        Order.RECEIVED,
        [("Veg Spring Rolls", 2), ("Dal Makhani", 1), ("Gulab Jamun", 2), ("Kulfi Falooda", 2)],
    ),
    (
        "Karan Malhotra", "9654321089", 10, "",
        Order.COMPLETED,
        [("Fish Amritsari", 1), ("Butter Chicken", 1), ("Garlic Naan", 3), ("Cold Coffee", 2)],
    ),
    (
        "Nisha Patel", "9543210978", 2, "Diabetic - less sugar in desserts",
        Order.COMPLETED,
        [("Paneer Butter Masala", 1), ("Garlic Naan", 2), ("Rasmalai", 1), ("Filter Coffee", 1)],
    ),
]


class Command(BaseCommand):
    help = "Load sample orders with order IDs and costs (safe to run once)."

    def handle(self, *args, **options):
        # Build a lookup by item name
        menu_items = {item.name: item for item in MenuItem.objects.all()}

        if not menu_items:
            self.stdout.write(self.style.ERROR(
                "No menu items found. Run `python manage.py seed_menu` first."
            ))
            return

        created = 0
        for customer_name, phone, table_number, notes, status, order_lines in SAMPLE_ORDERS:
            # Build cart dict as {str(pk): qty}
            cart = {}
            for item_name, qty in order_lines:
                item = menu_items.get(item_name)
                if not item:
                    self.stdout.write(self.style.WARNING(
                        f"  Skipped unknown item: {item_name}"
                    ))
                    continue
                if item.is_available:
                    cart[str(item.pk)] = qty

            if not cart:
                continue

            lines, subtotal, tax, total = calculate(cart)

            order = Order.objects.create(
                customer_name=customer_name,
                phone=phone,
                table_number=table_number,
                notes=notes,
                status=status,
                subtotal=subtotal,
                tax_amount=tax,
                total_amount=total,
            )

            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    menu_item=line["item"],
                    quantity=line["quantity"],
                    unit_price=line["item"].price,
                )
                for line in lines
            ])

            self.stdout.write(
                f"  Order #{order.pk:>3} | {customer_name:<18} | "
                f"Table {table_number:>2} | Rs.{total:>8} | {status}"
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone — {created} sample orders created."
        ))
