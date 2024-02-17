from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q, F
from django.contrib import messages
from .models import Product, Category
from django.db.models.functions import Lower
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist
from profiles.models import UserProfile

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
    user_profile = UserProfile.objects.get(user=request.user)
    wishlist = Wishlist.objects.get(user=user_profile)
    
    unique_category_ids = products.values_list('category', flat=True).distinct()
    categories = Category.objects.filter(id__in=unique_category_ids)
    
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            
            if sortkey == 'category':
                sortkey = 'category__name'
                products = products.annotate(category_name=F('category__name'))

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
        'category': category,
        'current_categories': categories,
        'current_designers': designers,
        'current_sorting': current_sorting,
        'wishlist': wishlist,
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

@login_required
def add_product(request):
    " Add a product to the store "
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Successfully added product!")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(request, "Failed to add product. Please ensure the form is valid.")
    else:         
        form = ProductForm()
    template = "products/add_product.html"
    context = {
        "form": form,
    }
    
    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))
    
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product in the store """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))