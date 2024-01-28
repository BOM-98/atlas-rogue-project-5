from django.shortcuts import render
from .models import Product, Category
from django.shortcuts import get_object_or_404

# Create your views here.
def all_products(request):
    """
    Render the products view.    
    """
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "products/products.html", context)

def product_detail(request, product_id):
    """
    Render the products detail view.
    """
    product = get_object_or_404(Product, pk=product_id)
    
    context = {
        "product": product,
    }
    return render(request, "products/product_detail.html", context)