from django.urls import path
from . import views


urlpatterns = [
    path('nav', views.navView, name='nav'),

    path('dashboard/', views.dashboardView, name='dashboard'),
    path('create_profile/<int:user_id>/', views.create_profileView, name='create_profile'),
    path('update_profile/<int:user_id>/', views.update_profileView, name='update_profile'),
    path('user_profile/<int:user_id>/', views.user_profileView, name='user_profile'),
    path('delete_profile/<int:user_id>/', views.delete_profileView, name='delete_profile'),


    path('create_or_update_profile/<int:user_id>/', views.create_or_update_profileView, name='create_or_update_profile'),



    path('customer_profile', views.customer_profileView, name='customer_profile'),
    path('payment_method', views.payment_methodView, name='payment_method'),
    path('add_appointment', views.add_appointmentView, name='add_appointment'),
    path('edit_appointment', views.edit_appointmentView, name='edit_appointment'),
    path('appointment_list', views.appointment_listView, name='appointment_list'),



    path('calendar/', views.calendarView, name='calendar'),
    path('get_events/', views.get_eventsView, name='get_events'),
    path('create_event/', views.create_eventView, name='create_event'),
    path('edit_event/<int:event_id>/', views.edit_eventView, name='edit_event'),
    path('delete_event/<int:event_id>/', views.delete_eventView, name='delete_event'),
    path('today_events/', views.today_eventsView, name='today_events'),
    path('past_events/', views.past_eventsView, name='past_events'),
    path('all_events/', views.all_eventsView, name='all_events'),
    
    path('search/', views.search_placesView, name='search_places'),
 

   
]