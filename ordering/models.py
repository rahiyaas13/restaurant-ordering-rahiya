from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional Bootstrap icon class, e.g. bi-cup-straw",
    )
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items"
    )
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    is_vegetarian = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Order(models.Model):
    RECEIVED = "received"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    STATUS_CHOICES = [
        (RECEIVED, "Received"),
        (PREPARING, "Preparing"),
        (READY, "Ready"),
        (COMPLETED, "Completed"),
    ]
    STATUS_FLOW = [RECEIVED, PREPARING, READY, COMPLETED]

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    table_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )
    notes = models.CharField(max_length=250, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=RECEIVED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - Table {self.table_number}"

    @property
    def status_index(self):
        return self.STATUS_FLOW.index(self.status)

    @property
    def next_status(self):
        i = self.status_index
        return self.STATUS_FLOW[i + 1] if i + 1 < len(self.STATUS_FLOW) else None

    @property
    def next_status_label(self):
        nxt = self.next_status
        return dict(self.STATUS_CHOICES)[nxt] if nxt else ""


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    @property
    def line_total(self):
        return self.unit_price * self.quantity
