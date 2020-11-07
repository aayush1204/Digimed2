from django.contrib import admin
from .models import Appointment, AttendsTO, Receptionist, Doctor, Patient
# Register your models here.
admin.site.register(Appointment)
admin.site.register(AttendsTO)
admin.site.register(Receptionist)
admin.site.register(Doctor)
admin.site.register(Patient)
