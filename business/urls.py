from django.urls import path
from . import views
#from .views import AppointmentDeleteView


urlpatterns = [
    path('business_dashboard/', views.business_dashboardView, name='business_dashboard'),
    path('for_business/', views.for_businessView, name='for_business'),
    path('add_client/', views.add_clientView, name='add_client'),
    path('edit_client/', views.edit_clientView, name='edit_client'),
    path('client_list/', views.client_listView, name='client_list'),

    path('catalog/', views.catalogView, name='catalog'),


    path('service_list/', views.service_list_view, name='service_list'),
    path('service_detail/<int:service_id>/', views.service_detail_view, name='service_detail'),
    path('service_create/', views.service_create_view, name='service_create'),
    path('service_update/<int:service_id>/', views.service_update_view, name='service_update'),
    path('service_delete/<int:service_id>/', views.service_delete_view, name='service_delete'),

    path('business_calendar/', views.business_calendar_view, name='business_calendar'),

    path('appointment_list/', views.appointment_list_view, name='appointment_list'),
    path('appointment_detail/<int:appointment_id>/', views.appointment_detail_view, name='appointment_detail'),
    path('appointment_create/', views.appointment_create_view, name='appointment_create'),
    path('appointment_update/<int:appointment_id>/', views.appointment_update_view, name='appointment_update'),
    path('appointment_delete/<int:appointment_id>/', views.appointment_delete_view, name='appointment_delete'),
    #path('appointment_delete/<int:appointment_id>/delete/', AppointmentDeleteView.as_view(), name='appointment_delete'),

    path('get_appointments/', views.get_appointments_view, name='get_appointments'),

    path('today_appointments/', views.today_appointments_view, name='today_appointments'),
    path('past_appointments/', views.past_appointments_view, name='past_appointments'),
    path('all_appointments/', views.all_appointments_view, name='all_appointments'),
    
    path('working_hours_list/', views.working_hours_list_view, name='working_hours_list'),
    #path('working_hours_detail/<int:working_hours_id>/', views.working_hours_detail_view, name='working_hours_detail'),
    path('working_hours_create/', views.working_hours_create_view, name='working_hours_create'),
    path('working_hours_update/<int:working_hours_id>/', views.working_hours_update_view, name='working_hours_update'),
    path('working_hours_delete/<int:working_hours_id>/', views.working_hours_delete_view, name='working_hours_delete'),


    path('catalog_list/', views.catalog_list_view, name='catalog_list'),
    path('catalog_detail/<int:catalog_id>/', views.catalog_detail_view, name='catalog_detail'),
    path('catalog_create/', views.catalog_create_view, name='catalog_create'),
    path('catalog_update/<int:catalog_id>/', views.catalog_update_view, name='catalog_update'),
    path('catalog_delete/<int:catalog_id>/', views.catalog_delete_view, name='catalog_delete'),
]
