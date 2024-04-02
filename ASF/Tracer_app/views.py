from django.shortcuts import render, redirect, get_object_or_404
from .models import ASFIncident, VeterinaryInspection, Quarantine, EpidemiologicalReport, BreedingFarm, MedicalResource
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .forms import AddASFIncidentForm, AdditionalInfoForm, InspectionAndQuarantineForm
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


class AddInspectionAndQuarantine(View):
    template_name = 'add_inspection_and_quarantine.html'
    form_class = InspectionAndQuarantineForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            inspection_date = form.cleaned_data['inspection_date']
            veterinarian = form.cleaned_data['veterinarian']
            results = form.cleaned_data['results']
            notes = form.cleaned_data['notes']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            location = form.cleaned_data['location']

            veterinary_inspection = VeterinaryInspection.objects.create(
                inspection_date=inspection_date,
                veterinarian=veterinarian,
                results=results,
                notes=notes
            )

            quarantine = Quarantine.objects.create(
                start_date=start_date,
                end_date=end_date,
                location=location
            )
            inspections = VeterinaryInspection.objects.all()
            quarantines = Quarantine.objects.all()

            return render(request, self.template_name,
                          {'form': form, 'inspections': inspections, 'quarantines': quarantines})
        return render(request, self.template_name, {'form': form})


class ShowInspectionsAndQuarantines(View):
    template_name = 'inspections_and_quarantines.html'

    def get(self, request):
        inspections = VeterinaryInspection.objects.all()
        quarantines = Quarantine.objects.all()
        return render(request, self.template_name, {'inspections': inspections, 'quarantines': quarantines})


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
            return redirect('/asf_incidents/')
        return render(request, self.template_name, {'form': form})


class AddAdditionalInfo(View):
    template_name = 'add_additional_info.html'
    form_class = AdditionalInfoForm

    def get(self, request):
        asf_incidents = ASFIncident.objects.all()
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'asf_incidents': asf_incidents})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            asf_incident_id = request.POST.get('asf_incident')
            epidemiological_report_description = form.cleaned_data['epidemiological_report_description']
            preventive_measures = form.cleaned_data['preventive_measures']
            breeding_farm_name = form.cleaned_data['breeding_farm_name']
            breeding_farm_address = form.cleaned_data['breeding_farm_address']
            pig_count = form.cleaned_data['pig_count']
            medical_resource_name = form.cleaned_data['medical_resource_name']
            quantity = form.cleaned_data['quantity']
            medical_resource_description = form.cleaned_data['medical_resource_description']

            asf_incident = ASFIncident.objects.get(id=asf_incident_id)

            epidemiological_report = EpidemiologicalReport.objects.create(
                report_date=asf_incident.detection_date,
                description=epidemiological_report_description,
                preventive_measures=preventive_measures,
                asf_incidents=asf_incident
            )

            breeding_farm = BreedingFarm.objects.create(
                name=breeding_farm_name,
                address=breeding_farm_address,
                pig_count=pig_count
            )
            breeding_farm.asf_incidents.add(asf_incident)

            medical_resource = MedicalResource.objects.create(
                name=medical_resource_name,
                quantity=quantity,
                description=medical_resource_description
            )
            medical_resource.asf_incidents.add(asf_incident)

            return redirect('confirmation')

        asf_incidents = ASFIncident.objects.all()
        return render(request, self.template_name, {'form': form, 'asf_incidents': asf_incidents})
