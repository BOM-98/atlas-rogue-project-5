from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from django.db.models.functions import Lower

# Create your views here.
def all_products(request):
    """
    Render the products view.    
    """
    products = Product.objects.all()
    query = None
    category = None
    designers = None
    categories = None
    sort = None
    direction = None
    
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
        
        if 'category' in request.GET:
            category = request.GET['category']
            products = products.filter(category__name__iexact=category)
            categories = Category.objects.filter(name__iexact=category)
            
        if 'designer' in request.GET:
            designer = request.GET['designer']
            products = products.filter(designer__iexact=designer)
            designers = Product.objects.filter(designer__iexact=designer)
        
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(category__name__icontains=query) | Q(designer__icontains=query) | Q(size__icontains=query) | Q(colour__icontains=query) | Q(length__icontains=query)
            products = products.filter(queries)
    
    current_sorting = f'{sort}_{direction}'
            
    context = {
        "products": products,
        'search_term': query,
        'current_categories': categories,
        'current_designers': designers,
        'current_sorting': current_sorting,
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