from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
from .models import *
from django.utils.html import escape
from django.template.loader import render_to_string
import logging
from datetime import datetime, time
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q



def business_dashboardView(request):
    return render(request, 'business/dashboard.html', context={})

def for_businessView(request):
    return render(request, 'business/business.html', context={})


def add_clientView(request):
    return render(request, 'business/add_client.html', context={})

def edit_clientView(request):
    return render(request, 'business/edit_client.html', context={})


def client_listView(request):
    return render(request, 'business/client_list.html', context={})


def catalogView(request):
    return render(request, 'business/catalog.html', context={})


#@login_required(login_url='login')
def service_list_view(request):
    services = Service.objects.filter(user=request.user)
    return render(request, 'business/service_list.html', {'services': services})

#@login_required(login_url='login')
def service_detail_view(request, service_id):
    service = get_object_or_404(Service, id=service_id, user=request.user)
    return render(request, 'business/service_detail.html', {'service': service})

#@login_required(login_url='login')
def service_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        # Validate and sanitize input
        if not name or not price:
            messages.error(request, 'Name and Price are required.')
            return redirect('service_list')

        # Sanitize user inputs
        name = escape(name)
        description = escape(description)

        # Create a new service
        service = Service.objects.create(
            user=request.user,
            name=name,
            description=description,
            price=price
        )

        messages.success(request, 'Service created successfully.')
        return redirect('service_list')

    return render(request, 'business/service_form.html', {'action': 'Create'})

#@login_required(login_url='login')
def service_update_view(request, service_id):
    service = get_object_or_404(Service, id=service_id, user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        # Validate and sanitize input
        if not name or not price:
            messages.error(request, 'Name and Price are required.')
            return redirect('service_list')

        # Sanitize user inputs
        name = escape(name)
        description = escape(description)

        # Update the service
        service.name = name
        service.description = description
        service.price = price
        service.save()

        messages.success(request, 'Service updated successfully.')
        return redirect('service_list')

    return render(request, 'business/service_form.html', {'action': 'Update', 'service': service})

#@login_required(login_url='login')
def service_delete_view(request, service_id):
    service = get_object_or_404(Service, id=service_id, user=request.user)
    
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully.')
        return redirect('service_list')

    return render(request, 'business/service_confirm_delete.html', {'service': service})


@login_required(login_url='login')
def business_calendar_view(request):
    return render(request, 'business/business_calendar.html')


@login_required(login_url='login')
def get_appointments_view(request):
    appointments = Appointment.objects.all()
    events = []

    for appointment in appointments:
        start_datetime = f"{appointment.date}T{appointment.time.strftime('%H:%M:%S')}"
        end_datetime = f"{appointment.date}T{appointment.time.strftime('%H:%M:%S')}"

        events.append({
            'id': appointment.id,
            'title': appointment.service.name,
            'start': start_datetime,
            'end': end_datetime,
            'date': appointment.date.strftime('%Y-%m-%d'),
            'time': appointment.time.strftime('%H:%M'),
            'note': appointment.note,
        })

    return JsonResponse(events, safe=False)



@login_required(login_url='login')
def appointment_list_view(request):
    # Retrieve all appointments for the logged-in user
    appointments = Appointment.objects.filter(user=request.user)

    context = {
        'appointments': appointments,
    }

    return render(request, 'business/appointment_list.html', context)


@login_required(login_url='login')
def appointment_detail_view(request, appointment_id):
    # Retrieve the appointment for the given appointment_id
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    context = {
        'appointment': appointment,
    }

    return render(request, 'business/appointment_detail.html', context)


@login_required(login_url='login')
def appointment_create_view(request):
    if request.method == 'POST':
        # Get form data
        service_id = request.POST.get('service')
        date = request.POST.get('date')
        time_str = request.POST.get('time')
        note = request.POST.get('note')

        # Print the received time string for debugging
        print(f'time_str: {time_str}')

        # Validate and sanitize input
        if not service_id or not date or not time_str:
            messages.error(request, 'All fields are required.')
            return redirect('appointment_list')

        try:
            # Convert the time string to a datetime.time object
            time_obj = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            messages.error(request, 'Invalid time format.')
            return redirect('appointment_list')

        # Sanitize user inputs using Django's escape function
        note = escape(note)

        # Create a new appointment
        appointment = Appointment.objects.create(
            user=request.user,
            service_id=service_id,
            date=date,
            time=time_obj,
            note=note
        )

        messages.success(request, 'Appointment created successfully.')
        return redirect('business_calendar')

    # Retrieve all services
    services = Service.objects.all()

    context = {
        'action': 'Create',
        'services': services,
    }


    return render(request, 'business/appointment_form.html', context)



@login_required(login_url='login')
def appointment_update_view(request, appointment_id):
    # Get the appointment instance
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    if request.method == 'POST':
        # Get form data
        service_id = request.POST.get('service')
        date = request.POST.get('date')
        time_str = request.POST.get('time')

        # Print the received time string for debugging
        print(f'time_str: {time_str}')

        # Print statements for debugging
        print(f'service_id: {service_id}')
        print(f'date: {date}')
        print(f'time_str: {time_str}')

        # Validate and sanitize input
        if not service_id or not date or not time_str:
            messages.error(request, 'All fields are required.')
            return redirect('appointment_list')

        try:
            # Convert the time string to a datetime.time object
            time_obj = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            messages.error(request, 'Invalid time format.')
            return redirect('appointment_list')

        # Print statement for debugging
        print(f'time_obj: {time_obj}')

        # Sanitize user inputs using Django's escape function
        note = escape(request.POST.get('note'))

        # Print statement for debugging
        print(f'note: {note}')

        # Update appointment
        appointment.service_id = service_id
        appointment.date = date
        appointment.time = time_obj
        appointment.note = note
        appointment.save()

        messages.success(request, 'Appointment updated successfully.')
        return redirect('appointment_list')

    # Retrieve all services
    services = Service.objects.all()

    context = {
        'action': 'Update',
        'appointment': appointment,
        'services': services,
        'selected_service_id': appointment.service_id,
    }

    return render(request, 'business/appointment_form.html', context)


@login_required(login_url='login')
def appointment_delete_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully.')
        return redirect('business_calendar')

    return render(request, 'business/appointment_confirm_delete.html', {'appointment': appointment})


@login_required(login_url='login')
def today_appointments_view(request):
    today = timezone.now().date()
    appointments = Appointment.objects.filter(user=request.user, date=today)

    context = {
        'appointments': appointments,
        'current_date': today,  # Add the current_date to the context
    }

    return render(request, 'business/today_appointments.html', context)


@login_required(login_url='login')
def past_appointments_view(request):
    today = timezone.now().date()
    past_appointments = Appointment.objects.filter(user=request.user, date__lt=today)

    context = {
        'appointments': past_appointments,  # Update the key to match the template variable
        'current_date': today,
    }

    return render(request, 'business/past_appointments.html', context)


@login_required(login_url='login')
def all_appointments_view(request):
    all_appointments = Appointment.objects.filter(user=request.user)

    context = {
        'all_appointments': all_appointments,
        'current_date': timezone.now().date(),  # Add the current_date to the context
    }

    return render(request, 'business/all_appointments.html', context)



@login_required(login_url='login')
def all_appointments_view(request):
    all_appointments = Appointment.objects.filter(user=request.user)

    context = {
        'all_appointments': all_appointments,
    }

    return render(request, 'business/all_appointments.html', context)






@login_required(login_url='login')
def working_hours_list_view(request):
    # Get the current day and time
    current_day = timezone.now().strftime('%A')  # e.g., 'Monday'
    current_time = timezone.now().strftime('%H:%M')  # e.g., '14:30'

    # Define the order of the days of the week
    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Get the working hours for the current user
    working_hours_list = Working_hours.objects.filter(user=request.user)

    # Order the working hours based on the custom order
    working_hours_list = sorted(working_hours_list, key=lambda wh: ordered_days.index(wh.day))

    return render(request, 'business/working_hours_list.html', {
        'working_hours_list': working_hours_list,
        'current_day': current_day,
        'current_time': current_time,
    })



@login_required(login_url='login')
def working_hours_create_view(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        opening_time = request.POST.get('opening_time')
        closing_time = request.POST.get('closing_time')
        additional_info = request.POST.get('additional_info')
        closed = request.POST.get('closed') == 'on'  # Check if 'closed' checkbox is checked

        # Validate and sanitize input
        if not day:
            messages.error(request, 'Day is required.')
            return redirect('working_hours_list')

        # Convert string time to datetime.time objects
        if opening_time:
            try:
                opening_time = datetime.strptime(opening_time, '%H:%M').time()
            except ValueError as e:
                messages.error(request, f'Invalid opening time format: {str(e)}')
                return redirect('working_hours_list')

        if closing_time:
            try:
                closing_time = datetime.strptime(closing_time, '%H:%M').time()
            except ValueError as e:
                messages.error(request, f'Invalid closing time format: {str(e)}')
                return redirect('working_hours_list')

        # Create a new working hours instance
        working_hours = Working_hours.objects.create(
            user=request.user,
            day=day,
            opening_time=opening_time if not closed else None,
            closing_time=closing_time if not closed else None,
            additional_info=additional_info,
            closed=closed
        )

        messages.success(request, 'Working hours created successfully.')
        return redirect('working_hours_list')

    # Pass choices for the 'day' field to the template
    day_choices = Working_hours.DAY_CHOICES
    return render(request, 'business/working_hours_form.html', {'action': 'Create', 'day_choices': day_choices})


@login_required(login_url='login')
def working_hours_update_view(request, working_hours_id):
    working_hours = get_object_or_404(Working_hours, id=working_hours_id, user=request.user)

    if request.method == 'POST':
        day = request.POST.get('day')
        opening_time = request.POST.get('opening_time')
        closing_time = request.POST.get('closing_time')
        additional_info = request.POST.get('additional_info')
        closed = request.POST.get('closed') == 'on'  # Check if 'closed' checkbox is checked

        # Validate and sanitize input
        if not day or (not opening_time and not closed) or (not closing_time and not closed):
            messages.error(request, 'All required fields must be filled.')
            return redirect('working_hours_list')

        # Convert string time to datetime.time objects
        try:
            opening_time = datetime.strptime(opening_time, '%H:%M').time() if opening_time else None
            closing_time = datetime.strptime(closing_time, '%H:%M').time() if closing_time else None
        except ValueError:
            messages.error(request, 'Invalid time format.')
            return redirect('working_hours_list')

        # Update working hours
        working_hours.day = day
        working_hours.opening_time = opening_time
        working_hours.closing_time = closing_time
        working_hours.additional_info = additional_info
        working_hours.closed = closed
        working_hours.save()

        messages.success(request, 'Working hours updated successfully.')
        return redirect('working_hours_list')

    # Pass choices for the 'day' field and current working hours to the template
    day_choices = Working_hours.DAY_CHOICES
    return render(request, 'business/working_hours_form.html', {'action': 'Update', 'working_hours': working_hours, 'day_choices': day_choices})


@login_required(login_url='login')
def working_hours_delete_view(request, working_hours_id):
    working_hours = get_object_or_404(Working_hours, id=working_hours_id, user=request.user)

    if request.method == 'POST':
        working_hours.delete()
        messages.success(request, 'Working hours deleted successfully.')
        return redirect('working_hours_list')

    return render(request, 'business/working_hours_confirm_delete.html', {'working_hours': working_hours})


@login_required(login_url='login')
def catalog_list_view(request):
    if request.user.is_authenticated and request.user.is_business:
        # Continue with the rest of your code
        catalogs = Catalog.objects.filter(user=request.user)
        services = Service.objects.all()
        appointments = Appointment.objects.all()
        ratings = Rating.objects.all()


        # Retrieve working hours for the current user
        working_hours_list = Working_hours.objects.filter(user=request.user)

        # Get the current day
        current_day = timezone.now().strftime('%A')  # e.g., 'Monday'

        # Define the order of the days of the week
        ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Order the working hours based on the custom order
        working_hours_list = sorted(working_hours_list, key=lambda wh: ordered_days.index(wh.day))

        context = {
            'catalogs': catalogs,
            'services': services,
            'appointments': appointments,
            'working_hours_list': working_hours_list,
            'current_day': current_day,
            'ratings': ratings,
        }

        return render(request, 'business/catalog_list.html', context)
    else:
        messages.info(request, "You are not authorized to view catalogs.")
        return redirect('/')  # Redirect to home or another page




@login_required(login_url='login')
def catalog_detail_view(request, catalog_id):
    catalog = get_object_or_404(Catalog, id=catalog_id, user=request.user)

    # Check if the user is a business
    if not request.user.is_business:
        messages.info(request, "You are not authorized to view catalog details.")
        return redirect('/')  # Redirect to home or another page

    return render(request, 'business/catalog_detail.html', {'catalog': catalog})



@login_required(login_url='login')
def catalog_create_view(request):
    if request.method == "POST":
        # Check if the user is a business
        if not (request.user.is_authenticated and request.user.is_business):
            messages.info(request, "You are not authorized to create a catalog.")
            return redirect('/')  # Redirect to home or another page

        username = request.user.username
        business_instance = User.objects.get(username=username)

        # Check file sizes
        catalog_cover_pic = request.FILES.get('business_cover_pic')
        catalog_logo = request.FILES.get('business_logo')
        if catalog_cover_pic and catalog_cover_pic.size > 2621440 or catalog_logo and catalog_logo.size > 2621440:
            messages.info(request, "The Catalog Cover Pic or Logo is bigger than 2MB.")
            return redirect('/add_catalog')

        # Check if catalog with the same business_name already exists
        if Catalog.objects.filter(business_name=request.POST.get('business_name')).exists():
            messages.info(request, "A catalog with this Business Name already exists.")
            return redirect('/catalog_create')

        # Extract form data
        business_name = request.POST.get('business_name')
        business_contact = request.POST.get('business_contact')
        bio = request.POST.get('bio')

        # Handle file uploads
        business_cover_pic = request.FILES.get('business_cover_pic')
        business_logo = request.FILES.get('business_logo')

        # Create a new catalog account
        create_new_catalog_account = Catalog.objects.create(
            business_name=business_name,
            business_contact=business_contact,
            bio=bio,
            business_cover_pic=business_cover_pic,
            business_logo=business_logo,
            user=business_instance  # Assuming 'user' is the ForeignKey in your Catalog model
        )

        messages.info(request, 'Catalog has been created successfully')

        # Retrieve and set the messages for the current request
        storage = messages.get_messages(request)
        storage.used = False

        return render(request, 'business/catalog_list.html', {'messages': storage})

    return render(request, 'business/catalog_form.html', {})





def catalog_update_view(request, catalog_id):
    if request.user.is_authenticated and request.user.is_business:
        catalog = get_object_or_404(Catalog, id=catalog_id, business=request.user)

        if request.method == "POST":
            # Extract form data from request.POST
            business_name = request.POST.get('business_name')
            business_contact = request.POST.get('business_contact')
            bio = request.POST.get('bio')

            # Handle file uploads
            business_cover_pic = request.FILES.get('business_cover_pic')
            business_logo = request.FILES.get('business_logo')

            # Update catalog fields
            catalog.business_name = business_name
            catalog.business_contact = business_contact
            catalog.bio = bio

            if business_cover_pic:
                catalog.business_cover_pic = business_cover_pic
            if business_logo:
                catalog.business_logo = business_logo

            catalog.save()

            messages.info(request, 'Catalog has been updated successfully')
            return redirect('catalog_list')  # Redirect to the catalog list page

        return render(request, 'business/catalog_form.html', {'catalog': catalog})
    else:
        messages.info(request, "You are not authorized to update catalogs.")
        return redirect('/')  # Redirect to home or another page


def catalog_delete_view(request, catalog_id):
    if request.user.is_authenticated and request.user.is_business:
        catalog = get_object_or_404(Catalog, id=catalog_id, business=request.user)
        catalog.delete()
        messages.info(request, 'Catalog has been deleted successfully')
        return redirect('catalog_list')  # Redirect to the catalog list page
    else:
        messages.info(request, "You are not authorized to delete catalogs.")
        return redirect('/')  # Redirect to home or another page


@login_required(login_url='login')
def rating_list_view(request):
    ratings = Rating.objects.filter(user=request.user)
    return render(request, 'business/rating_list.html', {'ratings': ratings})



@login_required(login_url='login')
def rating_create_view(request):
    if request.method == 'POST':
        salon_name = request.POST.get('salon_name')
        rating_value = request.POST.get('rating')
        comment = request.POST.get('comment')

        if salon_name and rating_value:
            # Assuming 'rating' is an IntegerField in your Rating model
            rating = Rating.objects.create(
                user=request.user,
                salon_name=salon_name,
                rating=int(rating_value),
                comment=comment
            )
            messages.success(request, 'Rating saved successfully.')
            return redirect('rating_list')

    return render(request, 'business/rating_form.html')

    
@login_required(login_url='login')
def rating_update_view(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id, user=request.user)

    if request.method == 'POST':
        salon_name = request.POST.get('salon_name')
        rating_value = request.POST.get('selected_rating')  # Updated to use the hidden input
        comment = request.POST.get('comment', '')

        if not salon_name or not rating_value:
            return HttpResponseBadRequest("Salon name and rating are required.")

        try:
            rating_value = int(rating_value)
        except ValueError:
            return HttpResponseBadRequest("Invalid rating value.")

        if rating_value < 1 or rating_value > 5:
            return HttpResponseBadRequest("Rating value must be between 1 and 5.")

        rating.salon_name = salon_name
        rating.rating = rating_value
        rating.comment = comment
        rating.save()

        return redirect('rating_list')

    return render(request, 'business/rating_form.html', {'rating': rating})


@login_required(login_url='login')
def rating_delete_view(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id, user=request.user)

    if request.method == 'POST':
        rating.delete()
        return redirect('rating_list')

    return render(request, 'business/rating_confirm_delete.html', {'rating': rating})

