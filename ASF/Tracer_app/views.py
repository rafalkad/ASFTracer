from django.shortcuts import render, redirect
from .models import ASFIncident, VeterinaryInspection, Quarantine, EpidemiologicalReport, BreedingFarm, MedicalResource
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .forms import AddASFIncidentForm, AdditionalInfoForm, InspectionAndQuarantineForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import folium
# Create your views here.


class ASFIncidentListView(View):
    def get(self, request):

        # View for displaying a list of ASF incidents.

        incidents = ASFIncident.objects.all().order_by('detection_date')

        location = request.GET.get('location')
        if location:
            incidents = incidents.filter(location__icontains=location)

        infected_count = request.GET.get('infected_count')
        if infected_count:
            try:
                incidents = incidents.filter(infected_count=int(infected_count))
            except ValueError:
                return HttpResponse("Invalid value for infected count.")

        context = {'incidents': incidents}
        return render(request, 'incident_list.html', context)


class AddInspectionAndQuarantine(View):

    #     View for adding inspections and quarantines.

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

            VeterinaryInspection.objects.create(
                inspection_date=inspection_date,
                veterinarian=veterinarian,
                results=results,
                notes=notes
            )

            Quarantine.objects.create(
                start_date=start_date,
                end_date=end_date,
                location=location
            )

            return redirect('show_inspections_and_quarantines')

        return render(request, self.template_name, {'form': form})


class ShowInspectionsAndQuarantines(View):

    #     View for displaying all inspections and quarantines.

    template_name = 'inspections_and_quarantines.html'

    def get(self, request):
        inspections = VeterinaryInspection.objects.all()
        quarantines = Quarantine.objects.all()
        return render(request, self.template_name, {'inspections': inspections, 'quarantines': quarantines})


class AddASFIncident(LoginRequiredMixin, View):

    #     View for adding ASF incidents.

    template_name = 'add_asfincident.html'
    form_class = AddASFIncidentForm
    login_url = '/admin/login/'

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

    #     View for adding additional information related to ASF incidents.

    template_name = 'add_additional_info.html'
    form_class = AdditionalInfoForm
    pdf_template_name = 'add_additional_info_pdf.html'

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

            context = {
                'epidemiological_report_description': epidemiological_report_description,
                'preventive_measures': preventive_measures,
                'breeding_farm_name': breeding_farm_name,
                'breeding_farm_address': breeding_farm_address,
                'pig_count': pig_count,
                'medical_resource_name': medical_resource_name,
                'quantity': quantity,
                'medical_resource_description': medical_resource_description,
            }
            html_string = render_to_string(self.pdf_template_name, context)

            pdf_file = HTML(string=html_string).write_pdf()

            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'filename="additional_info.pdf"'
            return response

        asf_incidents = ASFIncident.objects.all()

        return render(request, self.template_name, {'form': form, 'asf_incidents': asf_incidents})


class NotifyMailchimp(View):
    def get(self, request):

        # This view is responsible for sending notifications about the latest ASF
        # (African Swine Fever) incident to Mailchimp. It retrieves the latest ASF incident from the database,
        # prepares the necessary data to be sent to Mailchimp, and then sends a
        # POST request to the Mailchimp API to add a new subscriber to a specified mailing list.

        incidents = ASFIncident.objects.all().order_by('-detection_date')

        if incidents.exists():
            latest_incident = incidents.first()

            data = {
                "email_address": "piotrkowal@wp.pl",
                "status": "subscribed",
                "merge_fields": {
                    "FNAME": "Subscriber",
                    "LNAME": "ASF Incident Notification",
                    "INCIDENT_DATE": latest_incident.detection_date.strftime("%Y-%m-%d"),
                    "LOCATION": latest_incident.location,
                }
            }

            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": "8ea44a1870d330f3ebc80bc47229f6b2-us18",
                "server": "us18"
            })

            try:
                return HttpResponse("Notification sent to Mailchimp successfully.")
            except ApiClientError as error:
                return HttpResponse(f"Failed to send notification to Mailchimp: {error.text}", status=500)
        else:
            return HttpResponse("No ASF incidents found.", status=404)


class ASFMap(View):

    def get(self, request):

        # Generating  map and adding markers to the map

        map = folium.Map(location=[52.2297, 21.0122], zoom_start=10)

        folium.Marker([52.2297, 21.0122], popup='Warszawa').add_to(map)
        folium.Marker([52.0791, 21.0306], popup='<b>Piaseczno</b><br><i>Veterinary Inspection (2023-06-01)</i>').add_to(map)
        folium.Marker([51.3805, 23.5061], popup='<b>Łukcze</b><br><i>Veterinary Inspection (2023-06-01)</i>').add_to(map)
        folium.Marker([50.0134, 18.2208], popup='<b>Piekary</b><br><i>Veterinary Inspection (2023-06-01)</i>').add_to(map)
        folium.Marker([53.6136, 21.0062], popup='<b>Kleczkowo</b><br><i>Veterinary Inspection (2024-01-18)</i>').add_to(map)
        folium.Marker([52.2297, 21.0122], popup='Location A').add_to(map)
        folium.Marker([52.378, 19.267],   popup='Farm C').add_to(map)

        map_html = map._repr_html_()

        return render(request, 'asf_map.html', {'map_html': map_html})


