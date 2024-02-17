from django.shortcuts import render
from .models import Wishlist
from profiles.models import UserProfile
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
@login_required
def add_to_wishlist(request, product_id):
    product = Product.objects.get(pk=product_id)
    user = UserProfile.objects.get(user=request.user)
    wishlist, created = Wishlist.objects.get_or_create(user=user)

    # Check if the product is already in the wishlist
    if wishlist.products.filter(id=product_id).exists():
        messages.info(request, f"{product.name} is already in your wishlist.")
    else:
        wishlist.products.add(product)
        messages.info(request, f"{product.name} has been added to your wishlist.")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def view_wishlist(request):
    """
    View the user's wishlist. Create a wishlist if it does not exist.
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)
    wishlist, created = Wishlist.objects.get_or_create(user=user_profile)
    context = {
        "wishlist": wishlist.products.all(),
        "user": user_profile,
    }
    return render(request, "wishlist/wishlist.html", context)

@login_required
def remove_from_wishlist(request, product_id):
    """
    Remove a product from the user's wishlist
    """
    product = Product.objects.get(pk=product_id)
    user = UserProfile.objects.get(user=request.user)
    wishlist = Wishlist.objects.get(user=user)
    wishlist.products.remove(product)
    messages.info(request, f"{product.name} has been removed from your wishlist.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))