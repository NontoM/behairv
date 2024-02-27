from django.urls import path
from . import views


urlpatterns = [
    path('', views.homeView, name='home'),
    path('contact_us', views.contact_usView, name='contact_us'),
    path('faqs', views.faqsView, name='faqs'),
  

   
]