from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q, F
from django.contrib import messages
from .models import Product, Category
from django.db.models.functions import Lower
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist
from profiles.models import UserProfile


def all_products(request):
    """
    Render the products view.

    This function retrieves all products from the database
    and applies various filters and sorting options
    based on the user's request.
    It also handles search queries and displays the products accordingly.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered HTML template displaying the products.
    """
    products = Product.objects.all()
    query = None
    category = None
    designers = None
    categories = None
    sort = None
    direction = None
    wishlist = None

    unique_category_ids = products.values_list(
        'category', flat=True).distinct()
    categories = Category.objects.filter(
        id__in=unique_category_ids)

    # Only attempt to get the user's profile
    # and wishlist if the user is authenticated
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(
            user=request.user)
        wishlist, created = Wishlist.objects.get_or_create(
            user=user_profile)
    else:
        wishlist = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(
                    lower_name=Lower('name'))

            if sortkey == 'category':
                sortkey = 'category__name'
                products = products.annotate(
                    category_name=F('category__name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            category = request.GET['category']
            products = products.filter(
                category__name__iexact=category)
            categories = Category.objects.filter(
                name__iexact=category)

        if 'designer' in request.GET:
            designer = request.GET['designer']
            products = products.filter(
                designer__iexact=designer)
            designers = Product.objects.filter(
                designer__iexact=designer)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(
                name__icontains=query) | Q(
                    category__name__icontains=query) | Q(
                        designer__icontains=query) | Q(
                            size__icontains=query) | Q(
                                colour__icontains=query) | Q(
                                    length__icontains=query)
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

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product.

    Returns:
        HttpResponse: The rendered product detail view.
    """
    product = get_object_or_404(Product, pk=product_id)
    wishlist = None

    # Only attempt to get the user's
    # profile and wishlist if the user is authenticated
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        wishlist, created = Wishlist.objects.get_or_create(user=user_profile)
    else:
        wishlist = None

    context = {
        "product": product,
        "wishlist": wishlist,
    }
    return render(request, "products/product_detail.html", context)


@login_required
def add_product(request):
    """
    Add a product to the store

    This view function allows a logged-in user to add a product to the store.
    Only store owners (superusers) are allowed to perform this action.

    Parameters:
    - request: The HTTP request object

    Returns:
    - If the request method is POST and the form is valid, it
    redirects to the product detail page of the newly added product.
    - If the request method is POST and the form is invalid,
    it displays an error message and renders the add_product.html
    template with the invalid form.
    - If the request method is not POST, it renders
    the add_product.html template with an empty form.
    """
    if not request.user.is_superuser:
        messages.error(
            request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Successfully added product!")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request,
                "Failed to add product. Please ensure the form is valid.")
    else:
        form = ProductForm()
    template = "products/add_product.html"
    context = {
        "form": form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    Edit a product in the store.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to be edited.

    Returns:
        HttpResponse: The HTTP response object.

    Raises:
        Http404: If the product with the given ID does not exist.
    """
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
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid.')
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
    """
    Delete a product in the store

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to be deleted.

    Returns:
        HttpResponseRedirect: Redirects
        to the products page after successful deletion.

    Raises:
        Http404: If the product with the given ID does not exist.
    """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
