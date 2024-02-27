from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.register_pageView, name='register'),
    path('customer_register/', views.customerRegisterView, name="customer_register" ),
    path('business_register/', views.business_registerView, name="business_register" ),
    path('login/',views.loginView, name='login'),
   
    path('forgot_password/', views.forgot_passwordView, name="forgot_password" ),
    path('reset_password/', views.reset_passwordView, name="reset_password" ),

    path('logout/', views.log_outView, name='logout'),
    path('delete_account/', views.delete_accountView, name='delete_account'),



]