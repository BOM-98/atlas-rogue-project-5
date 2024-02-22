from django.shortcuts import render
from django.db import models
from products.models import Product, Category
from wishlist.models import Wishlist
from profiles.models import UserProfile


def index(request):
    """
    Render the homepage view.

    This view returns the homepage template for
    the website. It is a simple view that
    only renders the template without any
    additional context or processing.

    Parameters:
    request (HttpRequest): The HttpRequest
    object that represents the client's request.

    Returns:
    HttpResponse: An HttpResponse object
    that renders the 'home/index.html' template.
    """
    featured_product_1 = Product.objects.get(pk=49)
    featured_product_2 = Product.objects.get(pk=63)
    featured_product_3 = Product.objects.get(pk=66)
    featured_product_4 = Product.objects.get(pk=76)
    featured_products = [
        featured_product_1,
        featured_product_2,
        featured_product_3,
        featured_product_4]
    categories = Category.objects.all()
    wishlist = None

    # Only attempt to get the user's profile
    # and wishlist if the user is authenticated
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        wishlist, created = Wishlist.objects.get_or_create(user=user_profile)
    else:
        wishlist = None

    context = {
        "featured_products": featured_products,
        "current_categories": categories,
        "wishlist": wishlist,
    }
    return render(request, "home/index.html", context)


def about_us(request):
    """
    Render the about us view.

    This view returns the about us template for
    the website. It is a simple view that
    only renders the template without any
    additional context or processing.

    Parameters:
    request (HttpRequest): The HttpRequest
    object that represents the client's request.

    Returns:
    HttpResponse: An HttpResponse object
    that renders the 'home/about_us.html' template.
    """
    return render(request, "home/about_us.html")
