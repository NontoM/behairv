from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
from behairvauth.models import User
from .models import *
from django.db.models import Q
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .forms import UserProfileForm
from django.http import Http404

def navView(request):
    return render(request, 'nav.html')



def dashboardView(request):
    return render(request, 'customer/dashboard.html', context={})

@login_required
def create_profileView(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = Profile.objects.filter(user=user).first()

    if request.method == 'POST':
        # Process the form data here
        # Update the profile fields based on the submitted data

        # For example:
        profile.bio = request.POST.get('bio', '')
        profile.gender = request.POST.get('gender', '')
        address = request.POST.get('address', '')
        country = request.POST.get('country', '')
        city = request.POST.get('city', '')
        number = request.POST.get('number', '')
        email = request.POST.get('email', '')  # Add email field
        first_name = request.POST.get('first_name', '')  # Add first_name field
        last_name = request.POST.get('last_name', '')  # Add last_name field
        
        # Handle profile picture separately
        profile_picture = request.FILES.get('profile_picture')
        
        # Handle date_of_birth separately
        date_of_birth_str = request.POST.get('date_of_birth', '')
        if date_of_birth_str:
            # Parse the date string and convert it to the format Django expects
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            profile.date_of_birth = date_of_birth

        if not profile:
            # Create a new profile if it doesn't exist
            profile = Profile(user=user, gender=gender, bio=bio, profile_picture=profile_picture, date_of_birth=date_of_birth)
        else:
            # Update the existing profile
            profile.gender = gender
            profile.bio = bio
            profile.profile_picture = profile_picture
            profile.date_of_birth = date_of_birth

        # Update User model fields
        user.address = address
        user.country = country
        user.city = city
        user.number = number
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Save profile and user
        profile.save()
        messages.success(request, 'Profile created/updated successfully.')

    context = {'profile': profile, 'user_id': user.id}
    return render(request, 'customer/create_profile.html', context)



@login_required
def update_profileView(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = Profile.objects.filter(user=user).first()

    if request.method == 'POST':
        # Process the form data here
        # Update the profile fields based on the submitted data

        # For example:
        profile.bio = request.POST.get('bio', '')
        profile.gender = request.POST.get('gender', '')
        address = request.POST.get('address', '')
        country = request.POST.get('country', '')
        city = request.POST.get('city', '')
        number = request.POST.get('number', '')
        email = request.POST.get('email', '')  # Add email field
        first_name = request.POST.get('first_name', '')  # Add first_name field
        last_name = request.POST.get('last_name', '')  # Add last_name field

        # Handle date_of_birth separately
        date_of_birth_str = request.POST.get('date_of_birth', '')
        if date_of_birth_str:
            # Parse the date string and convert it to the format Django expects
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            profile.date_of_birth = date_of_birth
        # Handle profile picture upload if needed

        # Update User model fields
        user.address = address
        user.country = country
        user.city = city
        user.number = number
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        # Save the user model
        user.save()

        # Update the profile picture
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('update_profile', user_id=user.id)

    context = {
        'profile': profile,
        'user_id': user.id,
    }

    return render(request, 'customer/update_profile.html', context)



@login_required
def user_profileView(request, user_id):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    return render(request, 'customer/profile.html', {'user': user, 'profile': profile})


@login_required
def create_or_update_profileView(request, user_id=None):
    profile = Profile.objects.get(user=request.user)  # Assuming a one-to-one relationship
    
    if request.method == 'POST':
        # Update the user fields (assuming your User model has these fields)
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.username = request.POST.get('username', request.user.username)
        request.user.save()

        # Update the profile fields
        profile.date_of_birth = request.POST.get('date_of_birth', profile.date_of_birth)
        profile.gender = request.POST.get('gender', profile.gender)
        profile.number = request.POST.get('number', profile.number)

        # Handle profile picture separately due to file upload
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        # Update the location fields
        profile.address = request.POST.get('address', profile.address)
        profile.location_number = request.POST.get('location_number', profile.location_number)
        profile.city = request.POST.get('city', profile.city)
        profile.country = request.POST.get('country', profile.country)
        profile.zip_code = request.POST.get('zip_code', profile.zip_code)

        # Update the bio field
        profile.bio = request.POST.get('bio', profile.bio)

        profile.save()
        return redirect('user_profile', user_id=request.user.id)

    # Assuming you have a template variable called 'profile' for the user's profile
    return render(request, 'customer/create_or_update_profile.html', {'user': request.user, 'profile': profile})



@login_required
def delete_profileView(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    try:
        profile = Profile.objects.get(user=user)
        profile.delete()
        messages.success(request, 'Profile deleted successfully.')
    except Profile.DoesNotExist:
        messages.error(request, 'Profile not found.')
    except Exception as e:
        messages.error(request, f'Error deleting profile: {str(e)}')

    return redirect('register')


@login_required
def calendarView(request):
    return render(request, 'customer/calendar.html')


@login_required
def get_eventsView(request):
    events = Event.objects.all()
    event_data = []

    for event in events:
        event_data.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
        })

    return JsonResponse(event_data, safe=False)


@login_required
def create_eventView(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_time = timezone.make_aware(datetime.strptime(request.POST.get('start_time'), '%Y-%m-%dT%H:%M'))
        end_time = timezone.make_aware(datetime.strptime(request.POST.get('end_time'), '%Y-%m-%dT%H:%M'))

        if not title or not start_time or not end_time:
            return JsonResponse({'message': 'All fields are required', 'status': 'error'}, status=400)

        new_event = Event.objects.create(title=title, start_time=start_time, end_time=end_time)

        event_data = {
            'id': new_event.id,
            'title': new_event.title,
            'start': new_event.start_time.isoformat(),
            'end': new_event.end_time.isoformat(),
        }

        return JsonResponse({'message': 'Event created successfully', 'event': event_data, 'status': 'success'})

    return JsonResponse({'message': 'Invalid request', 'status': 'error'}, status=400)


@login_required
def edit_eventView(request, event_id):
    print(f"Received request to edit event with ID {event_id}")
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        start_time = timezone.make_aware(datetime.strptime(request.POST.get('start_time'), '%Y-%m-%dT%H:%M'))
        end_time = timezone.make_aware(datetime.strptime(request.POST.get('end_time'), '%Y-%m-%dT%H:%M'))

        if not title or not start_time or not end_time:
            return JsonResponse({'message': 'All fields are required', 'status': 'error'})

        event.title = title
        event.start_time = start_time
        event.end_time = end_time
        event.save()

        updated_event = {
            'id': event.id,
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
        }

        return JsonResponse({'message': 'Event updated successfully', 'event': updated_event, 'status': 'success'})

    return JsonResponse({'message': 'Invalid request', 'status': 'error'})

@login_required
def delete_eventView(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event deleted successfully', 'status': 'success'})

    return JsonResponse({'message': 'Invalid request', 'status': 'error'})


@login_required
def today_eventsView(request):
    current_date = timezone.now().date()
    events = Event.objects.filter(start_time__date=current_date)
    return render(request, 'customer/today_events.html', {'events': events, 'current_date': current_date})


@login_required
def past_eventsView(request):
    current_date = timezone.now()
    past_events = Event.objects.filter(end_time__lt=current_date)
    return render(request, 'customer/past_events.html', {'past_events': past_events, 'current_date': current_date})


@login_required
def all_eventsView(request):
    all_events = Event.objects.all()
    return render(request, 'customer/all_events.html', {'all_events': all_events})


# search
def search_placesView(request):
    categories = Category.objects.all()
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')
    keywords = request.GET.get('keywords', '')

    errors = []

    if request.method == 'GET' and (not category and not location and not keywords):
        errors.append("Please enter a category, location, or keywords to search.")

    places = Place.objects.all()

    if category:
        places = places.filter(category=category)

    if location:
        places = places.filter(location__icontains=location)

    if keywords:
        # Assuming you want to search in the Place model fields for keywords
        places = places.filter(Q(location__icontains=keywords) | Q(category__name__icontains=keywords))

    if not places:
        errors.append("No results found for the given search criteria.")

    return render(request, 'customer/search_form.html', {'categories': categories, 'errors': errors,
                                                        'category': category, 'location': location,
                                                        'keywords': keywords, 'places': places})




def customer_profileView(request):
    return render(request, 'customer/profile.html', context={})

def payment_methodView(request):
    return render(request, 'customer/payment_method.html', context={})

def add_appointmentView(request):
    return render(request, 'customer/add_appointment.html', context={})

def edit_appointmentView(request):
    return render(request, 'customer/edit_appointment.html', context={})


def appointment_listView(request):
    return render(request, 'customer/appointment_list.html', context={})


