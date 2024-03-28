from django import forms
from .models import ASFIncident

class AddASFIncidentForm(forms.ModelForm):
    class Meta:
        model = ASFIncident
        fields = ['detection_date', 'location', 'infected_count', 'veterinary_inspections', 'quarantines']