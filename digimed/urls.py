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
    path('doctor-view-records', views.doctor_view_records,name='doctor-view-records'),
    path('doctor-view-records-single/<slug:a>', views.doctor_view_records_single,name='doctor-view-records-single'),
    path('doctor-prescription-add/<slug:p>', views.doctor_prescription_add,name='doctor-prescription-add'),
    path('doctor-add-symptom/<slug:p>', views.doctor_prescription_add_symptom,name='doctor-add-symptom'),
    path('doctor-delete-symptom/<slug:p>/<slug:a>', views.doctor_prescription_delete_symptom,name='doctor-delete-symptom'),
    path('doctor-delete-medicaltest/<slug:p>/<slug:a>', views.doctor_prescription_delete_medicaltest,name='doctor-delete-medicaltest'),
    path('doctor-delete-medicines/<slug:p>/<slug:a>', views.doctor_prescription_delete_medicines,name='doctor-delete-medicines'),
    path('doctor-add-medicaltest/<slug:p>', views.doctor_prescription_add_medicaltest,name='doctor-add-medicaltest'),
    path('doctor-add-medicines/<slug:p>', views.doctor_prescription_add_medicines,name='doctor-add-medicines'),
    # path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    # path('delete-appointment/<slug:pk>', views.delete_appointment_view,name='delete-appointment'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),
    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),



    path('patientclick', views.patientclick_view),
    path('patientsignup', views.patient_signup_view),
    path('patientregister', views.patient_signup_view,name='patientregister'),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),
    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-view-records', views.patient_view_records,name='patient-view-records'),
    path('patient-records', views.patient_records,name='patient-records'),
    path('patient-upload-records', views.patient_upload_records,name='patient-upload-records'),
    path('patient-doctors', views.patient_doctors,name='patient-doctors'),
    path('patient-view-doctors', views.patient_view_doctors,name='patient-view-doctors'),
    path('patient-add-doctors', views.patient_add_doctors,name='patient-add-doctors'),

    path('patient-prescription-view/<slug:p>', views.patient_prescription_view,name='patient-prescription-view'),
    path('patient-appointment', views.patient_appointments,name='patient-appointment'),
    path('patient-view-appointments', views.patient_view_appointments,name='patient-view-appointments'),
    path('patient-book-appointments', views.patient_add_appointments,name='patient-book-appointments'),

    path('adminclick', views.adminclick_view),
    path('adminsignup', views.admin_signup_view),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),

]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
