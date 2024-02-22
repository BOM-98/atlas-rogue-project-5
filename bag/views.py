from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from products.models import Product
from django.contrib import messages
from datetime import datetime


# Create your views here.
def view_bag(request):
    """
    Render the cart view.

    This view returns the cart template for
    the website. It is a simple view that
    only renders the template without any
    additional context or processing.
    """
    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """
    Add a quantity of the specified product to the shopping bag.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the product to add to the bag.

    Returns:
        HttpResponseRedirect: A redirect response to the specified URL.

    Raises:
        None
    """
    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get("quantity"))
    start_date_str = request.POST.get('start_date')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date_str = request.POST.get('end_date')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    redirect_url = request.POST.get("redirect_url")
    bag = request.session.get("bag", {})

    # Calculating the difference
    difference = end_date - start_date

    # Getting the number of days
    number_of_days = difference.days
    quantity = number_of_days

    # Validate that both start_date and end_date are provided
    if not start_date or not end_date:
        messages.error(
            request, "You must select both a start and an end date.")
        return redirect('product_detail', product_id=item_id)

    # Convert date objects to string in ISO
    # format before storing in the session
    if start_date:
        start_date = start_date.isoformat()  # Converts to 'YYYY-MM-DD' string
    if end_date:
        end_date = end_date.isoformat()

    if item_id in list(bag.keys()):
        bag[item_id] = {
            'quantity': quantity,
            'start_date': start_date,
            'end_date': end_date}
    else:
        bag[item_id] = {
            'quantity': quantity,
            'start_date': start_date,
            'end_date': end_date}
    bag[item_id] = {
        'quantity': quantity,
        'start_date': start_date,
        'end_date': end_date}
    messages.success(request, f"Added {product.name} to your bag")

    request.session["bag"] = bag
    return redirect(redirect_url)


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the item to be removed from the bag.

    Returns:
        HttpResponseRedirect: Redirects to the 'view_bag' view.

    Raises:
        HttpResponse: If there is an error removing the item.
    """
    try:
        product = Product.objects.get(pk=item_id)
        bag = request.session.get('bag', {})
        bag.pop(item_id)
        request.session['bag'] = bag
        messages.error(request, f"Removed {product.name} from your bag")
        return redirect('view_bag')
    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return HttpResponse(status=500)
