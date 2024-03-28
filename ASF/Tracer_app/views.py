from django.shortcuts import render, redirect
from .models import ASFIncident
from django.http import HttpResponse
from .forms import AddASFIncidentForm
from django.views import View
# Create your views here.
def asf_incident_list(request):
    incidents = ASFIncident.objects.all()
    incidents = incidents.order_by('detection_date')

    if 'location' in request.GET:
        location = request.GET['location']
        incidents = incidents.filter(location__icontains=location)

    if 'infected_count' in request.GET:
        infected_count = request.GET['infected_count']
        try:
            incidents = incidents.filter(infected_count=int(infected_count))
        except ValueError:
            return HttpResponse("Invalid value for infected count.")

    context = {
        'incidents': incidents
    }

    return render(request, 'incident_list.html', context)

class AddASFIncident(View):
    template_name = 'add_asfincident.html'
    form_class = AddASFIncidentForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            detection_date = form.cleaned_data['detection_date']
            location = form.cleaned_data['location']
            infected_count = form.cleaned_data['infected_count']
            veterinary_inspections = form.cleaned_data['veterinary_inspections']
            quarantines = form.cleaned_data['quarantines']

            ASFIncident.objects.create(
                detection_date=detection_date,
                location=location,
                infected_count=infected_count,
                veterinary_inspections=veterinary_inspections,
                quarantines=quarantines
            )
            return redirect('/asf_incident_list/')
        return render(request, self.template_name, {'form': form})
