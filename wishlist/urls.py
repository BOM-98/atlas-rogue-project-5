from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("add_to_wishlist/<int:product_id>", views.add_to_wishlist, name="add_to_wishlist"),
    path("view_wishlist/", views.view_wishlist, name="wishlist"),
    path("remove_from_wishlist/<int:product_id>", views.remove_from_wishlist, name="remove_from_wishlist"),
]