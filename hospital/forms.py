from django import forms
from .models import Description,AttendsTO

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
