from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from bag.contexts import bag_contents
import stripe
from django.conf import settings
import os


def checkout(request):
    """
    A view to return the checkout page
    """
    # Load Stripe keys from environment variables
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    stripe_public_key = os.getenv("STRIPE_PUBLIC_KEY")

    bag = request.session.get("bag", {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse("products"))

    current_bag = bag_contents(request)
    total = current_bag["grand_total"]
    stripe_total = round(total * 100)  # Stripe requires the amount to be in cents

    # Create a Stripe PaymentIntent
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency="usd",
        # Add any additional arguments here
    )

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(
            request,
            "Stripe public key is missing. \
            Did you forget to set it in your environment?",
        )

    template = "checkout/checkout.html"
    context = {
        "order_form": order_form,
        "stripe_public_key": stripe_public_key,
        "client_secret": intent.client_secret,
    }
    return render(request, template, context)
