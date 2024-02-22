from django.shortcuts import render


def handler404(request, exception):
    """ Error Handler 404 - Page Not Found

    This function handles the 404 error, which occurs when a page is not found.

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception object representing the error.

    Returns:
        HttpResponse: The rendered 404 error page.
    """
    return render(request, "errors/404.html", status=404)
