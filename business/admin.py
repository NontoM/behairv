from django.contrib import admin
from .models import Service, Appointment, Working_hours, Catalog, Rating

# Register your models here.

admin.site.register(Service)
admin.site.register(Appointment)
admin.site.register(Working_hours)
admin.site.register(Catalog)
admin.site.register(Rating)


