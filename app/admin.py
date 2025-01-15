from django.contrib import admin
from .models import Admin, Customer, Therapist, Service, Appointment, Availability

# Register your models here.
admin.site.register(Admin),
admin.site.register(Customer),
admin.site.register(Therapist),
admin.site.register(Service),
admin.site.register(Appointment),
admin.site.register(Availability),
