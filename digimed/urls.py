"""digimed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    path('doctorclick', views.doctorclick_view),
    path('doctorsignup', views.doctor_signup_view,name='doctorsignup'),
    path('doctorregister', views.doctor_signup_view,name='doctorregister'),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-prescription-add/<slug:p>', views.doctor_prescription_add,name='doctor-prescription-add'),
    path('doctor-add-symptom/<slug:p>', views.doctor_prescription_add_symptom,name='doctor-add-symptom'),
    path('doctor-add-medicaltest/<slug:p>', views.doctor_prescription_add_medicaltest,name='doctor-add-medicaltest'),
    path('doctor-add-medicines/<slug:p>', views.doctor_prescription_add_medicines,name='doctor-add-medicines'),
    # path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    # path('delete-appointment/<slug:pk>', views.delete_appointment_view,name='delete-appointment'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),

    path('patientclick', views.patientclick_view),
    path('patientsignup', views.patient_signup_view),
    path('patientregister', views.patient_signup_view,name='patientregister'),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),
    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-view-records', views.patient_view_records,name='patient-view-records'),
    path('patient-records', views.patient_records,name='patient-records'),
    path('patient-upload-records', views.patient_upload_records,name='patient-upload-records'),

    path('adminclick', views.adminclick_view),
    path('adminsignup', views.admin_signup_view),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),

]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
