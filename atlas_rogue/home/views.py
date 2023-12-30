from django.shortcuts import render

# Create your views here.
def index(request):
    """
    Render the homepage view.

    This view returns the homepage template for
    the website. It is a simple view that
    only renders the template without any
    additional context or processing.

    Parameters:
    request (HttpRequest): The HttpRequest
    object that represents the client's request.

    Returns:
    HttpResponse: An HttpResponse object
    that renders the 'home/index.html' template.
    """

    return render(request, "home/index.html")