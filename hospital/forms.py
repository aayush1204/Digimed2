from django import forms
from .models import Description,AttendsTO,Appointment

class UploadRecordForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ['recimage','type','title','rid']
        widgets = {'rid': forms.HiddenInput()}

class AddDoctorForm(forms.ModelForm):
    class Meta:
        model = AttendsTO
        fields = ['pid','did']
        widgets = {'pid': forms.HiddenInput()}

class AddAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointmentId','patientId','receptionistid','doctorId','date','timing']
        widgets = {'appointmentId': forms.HiddenInput(),
                   'patientId': forms.HiddenInput(),
                   'receptionistid' : forms.HiddenInput()
                  }
