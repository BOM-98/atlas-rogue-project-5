from django.shortcuts import render, redirect, reverse
from .forms import ContactForm
from django.contrib import messages
from .models import Contact
from django.http import HttpResponseForbidden

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    template = 'contact/contact.html'
    return render(request, template, {'form': form})

def contact_submissions(request):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you do not have permission to view this page.')
        return redirect(reverse("home"))
    contacts = Contact.objects.all()
    template = 'contact/contact_form_submissions.html'
    context = {
        'contacts': contacts,
    }
    return render(request, template, context)