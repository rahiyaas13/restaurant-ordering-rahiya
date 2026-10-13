import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True)),
                ("icon", models.CharField(blank=True, help_text="Optional Bootstrap icon class, e.g. bi-cup-straw", max_length=50)),
                ("display_order", models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                "verbose_name_plural": "categories",
                "ordering": ["display_order", "name"],
            },
        ),
        migrations.CreateModel(
            name="MenuItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal("0.01"))])),
                ("is_vegetarian", models.BooleanField(default=False)),
                ("is_available", models.BooleanField(default=True)),
                ("image_url", models.URLField(blank=True, max_length=500)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="ordering.category")),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_name", models.CharField(max_length=100)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("table_number", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)])),
                ("notes", models.CharField(blank=True, max_length=250)),
                ("subtotal", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("tax_amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("total_amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("status", models.CharField(choices=[("received", "Received"), ("preparing", "Preparing"), ("ready", "Ready"), ("completed", "Completed")], default="received", max_length=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)])),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("menu_item", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="order_items", to="ordering.menuitem")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="ordering.order")),
            ],
        ),
    ]
