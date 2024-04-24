from django import forms
from .models import ASFIncident


class InspectionAndQuarantineForm(forms.Form):
    inspection_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    veterinarian = forms.CharField(max_length=100)
    results = forms.CharField(widget=forms.Textarea)
    notes = forms.CharField(widget=forms.Textarea)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    location = forms.CharField(max_length=100)


class AddASFIncidentForm(forms.ModelForm):
    class Meta:
        model = ASFIncident
        fields = ['detection_date', 'location', 'infected_count', 'veterinary_inspections', 'quarantines']
        widgets = {
            'detection_date': forms.DateInput(attrs={'type': 'date'})
        }


class AdditionalInfoForm(forms.Form):
    epidemiological_report_description = forms.CharField(label="Epidemiological Report Description", widget=forms.Textarea)
    preventive_measures = forms.CharField(label="Preventive Measures", widget=forms.Textarea)
    breeding_farm_name = forms.CharField(label="Breeding Farm Name", max_length=100)
    breeding_farm_address = forms.CharField(label="Breeding Farm Address", max_length=200)
    pig_count = forms.IntegerField(label="Pig Count")
    medical_resource_name = forms.CharField(label="Medical Resource Name", max_length=100)
    quantity = forms.IntegerField(label="Quantity")
    medical_resource_description = forms.CharField(label="Description", widget=forms.Textarea)

