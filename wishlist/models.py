from django.db import models
from django.conf import settings
from products.models import Product
from profiles.models import UserProfile


class Wishlist(models.Model):
    """
    Represents a user's wishlist.

    Attributes:
        user (UserProfile): The user
        who owns the wishlist.
        products (ManyToManyField):
        The products added to the wishlist.
    """
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(
        Product, related_name='wishlisted_by')
