from django.shortcuts import render

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