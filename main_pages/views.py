from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
from customer.models import Category, Place


def homeView(request):
    categories = Category.objects.all()
    locations = Place.objects.values_list('location', flat=True).distinct()

    return render(request, 'main_pages/home.html', {'categories': categories, 'locations': locations})


def contact_usView(request):
    return render(request, 'main_pages/contact_us.html', context={})


def faqsView(request):
    return render(request, 'main_pages/faqs.html', context={})
