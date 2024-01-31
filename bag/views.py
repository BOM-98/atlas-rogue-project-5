from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

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
    """ Add a quantity of the specified product to the shopping bag """
    
    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url")
    bag = request.session.get("bag", {})
    
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
    bag[item_id] = quantity
    
    request.session["bag"] = bag
    return redirect(redirect_url)

def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        bag = request.session.get('bag', {})
        bag.pop(item_id)
        request.session['bag'] = bag
        return redirect('view_bag')
    except Exception as e:
        return HttpResponse(status=500)