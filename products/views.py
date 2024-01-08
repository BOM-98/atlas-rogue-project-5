from django.shortcuts import render
from .models import Product, Category

# Create your views here.
def all_products(request):
    """
    Render the products view.

    This view returns the homepage template for
    the website. It is a simple view that
    only renders the template without any
    additional context or processing.

    Parameters:
    request (HttpRequest): The HttpRequest
    object that represents the client's request.

    Returns:
    HttpResponse: An HttpResponse object
    that renders the 'products/products.html' template.
    """
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "products/products.html", context)