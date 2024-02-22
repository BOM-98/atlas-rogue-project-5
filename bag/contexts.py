from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from datetime import datetime


def bag_contents(request):
    """
    A view to return the bag contents page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary containing the bag items, total price,
        product count, delivery cost,
        free delivery threshold, and grand total.

    """
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get("bag", {})

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        start_date = item_data['start_date']
        end_date = item_data['end_date']
        item_total = item_data['quantity'] * product.price
        total += item_data['quantity'] * product.price
        product_count += item_data['quantity']
        bag_items.append({
            "item_id": item_id,
            "quantity": item_data['quantity'],
            "product": product,
            "item_total": item_total,
            "start_date": start_date,
            "end_date": end_date,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "grand_total": grand_total,
    }
    return context
