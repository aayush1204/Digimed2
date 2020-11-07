from django.contrib import admin
from .models import Appointment,Patient, PhoneNumber, AttendsTO, Prescription, Symptoms, Doctor, PrescribedIn
# Register your models here.
admin.site.register(Appointment)
admin.site.register(AttendsTO)
admin.site.register(Prescription)
admin.site.register(Symptoms)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(PrescribedIn)
admin.site.register(PhoneNumber)
