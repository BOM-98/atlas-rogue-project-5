from django.urls import path
from . import views

urlpatterns = [
    path('contact_form/', views.contact, name='contact'),
    path('contact_submissions/', views.contact_submissions, name='contact_submissions'),
]