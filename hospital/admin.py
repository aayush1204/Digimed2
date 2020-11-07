from django.contrib import admin
from .models import Appointment, AttendsTO, Description, Records, Doctor
# Register your models here.
admin.site.register(Appointment)
admin.site.register(AttendsTO)
admin.site.register(Records)
admin.site.register(Description)
admin.site.register(Doctor)
