from django.contrib import admin

from .models import Category, MenuItem, Order, OrderItem

# ── PLUVIA admin branding ────────────────────────────────────────────────────
admin.site.site_header = "PLUVIA Admin"
admin.site.site_title  = "PLUVIA"
admin.site.index_title = "PLUVIA Restaurant — Management"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "display_order")
    list_editable = ("display_order",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_vegetarian", "is_available")
    list_filter = ("category", "is_vegetarian", "is_available")
    list_editable = ("price", "is_available")
    search_fields = ("name", "description")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("unit_price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "table_number", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    list_editable = ("status",)
    search_fields = ("id", "customer_name", "phone")
    readonly_fields = ("subtotal", "tax_amount", "total_amount", "created_at", "updated_at")
    inlines = [OrderItemInline]
