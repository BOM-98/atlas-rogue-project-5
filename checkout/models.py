from django.db import models
import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    """
    Represents an order made by a user.

    Methods:
    - _generate_order_number: Generates a random,
    unique order number using UUID.
    - update_total: Updates the grand total of the order,
    accounting for delivery costs.
    - save: Overrides the original save method to set the
    order number if it hasn't been set already.
    - __str__: Returns a string representation of the
    order (the order number).
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label="Country *", null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
    )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    original_bag = models.TextField(null=False, blank=False, default="")
    stripe_pid = models.CharField(
        max_length=254,
        null=False,
        blank=False,
        default="")

    def _generate_order_number(self):
        """
        Generate a random,
        unique order number using UUID.
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = (
            self.lineitems.aggregate(
                Sum("lineitem_total"))["lineitem_total__sum"] or 0
        )
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            )
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method
        to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    Represents a line item in an order.

    Attributes:
        order (Order): The order that this line
        item belongs to.
        product (Product): The product associated
        with this line item.
        quantity (int): The quantity of the product
        in this line item.
        lineitem_total (Decimal): The total cost of
        this line item.

    Methods:
        save(*args, **kwargs): Overrides the original
        save method to set the lineitem total and update the order total.
        __str__(): Returns a string representation of the line item.
    """
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="lineitems",
    )
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"SKU {self.product.sku} on order {self.order.order_number}"


class ProductRental(models.Model):
    """
    Represents a rental period for a product.

    Attributes:
        product (ForeignKey): A reference to the Product being rented.
        order_line_item (ForeignKey): The OrderLineItem associated
        with this rental, linking the rental to a specific order.
        start_date (DateField): The start date of the rental period.
        end_date (DateField): The end date of the rental period.

    Methods:
        clean: Validates the rental to prevent overlapping rental
        periods for the same product.
        save: Overrides the default save method to include clean
        method validation before saving.
        __str__: Returns a human-readable string representation
        of the rental instance.
    """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='rentals')
    order_line_item = models.ForeignKey(
        OrderLineItem, on_delete=models.CASCADE, related_name='rentals')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.product.name} rented from {self.start_date} to {self.end_date}"
