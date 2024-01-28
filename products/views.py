from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.
def all_products(request):
    """
    Render the products view.    
    """
    products = Product.objects.all()
    query = None
    
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(category__name__icontains=query) | Q(designer__icontains=query) | Q(size__icontains=query) | Q(colour__icontains=query) | Q(length__icontains=query)
            products = products.filter(queries)
            
        context = {
            "products": products,
            'search_term': query,
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