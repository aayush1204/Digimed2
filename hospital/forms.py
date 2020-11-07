from django import forms
from .models import Description

class UploadRecordForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ['recimage','type','title','rid']
        widgets = {'rid': forms.HiddenInput()}
