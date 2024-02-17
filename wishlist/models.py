from django.db import models
from django.conf import settings
from products.models import Product
from profiles.models import UserProfile

class Wishlist(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, related_name='wishlisted_by')