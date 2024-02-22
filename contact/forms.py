from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    A form for creating a contact message.

    Attributes:
        name (str): The name of the user.
        email (str): The email address of the user.
        subject (str): The subject of the contact message.
        message (str): The content of the contact message.
    """

    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
