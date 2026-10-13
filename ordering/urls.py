from django.urls import path

from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path("cart/", views.cart, name="cart"),
    path("cart/sync/", views.cart_sync, name="cart_sync"),
    path("checkout/", views.checkout, name="checkout"),
    path("track/", views.track_lookup, name="track_lookup"),
    path("track/<int:pk>/", views.track_order, name="track_order"),
    path("kitchen/", views.kitchen, name="kitchen"),
    path("kitchen/<int:pk>/status/", views.kitchen_update, name="kitchen_update"),
]
