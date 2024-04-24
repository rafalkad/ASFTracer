import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ASFIncident, VeterinaryInspection, Quarantine



# Create your tests here.


@pytest.fixture
def client():
    return Client()

@pytest.fixture
def sample_asf_incidents():
    ASFIncident.objects.create(detection_date='2024-01-01', location='Location A', infected_count=5)
    ASFIncident.objects.create(detection_date='2024-02-01', location='Location B', infected_count=10)

@pytest.mark.first
def test_asf_incident_list_view(client, sample_asf_incidents):
    response = client.get(reverse('asf_incident_list'))
    assert response.status_code == 200
    assert len(response.context['incidents']) == 2

@pytest.mark.second
def test_filter_by_location(client, sample_asf_incidents):
    response = client.get(reverse('asf_incident_list'), {'location': 'Location A'})
    assert response.status_code == 200
    assert len(response.context['incidents']) == 1

@pytest.mark.third
def test_add_inspection_and_quarantine_get(client):
    response = client.get(reverse('add_inspection_and_quarantine'))
    assert response.status_code == 200

@pytest.mark.fourth
def test_add_inspection_and_quarantine_post(client):
    data = {
        'inspection_date': '2024-04-04',
        'veterinarian': 'Test Vet',
        'results': 'Test Results',
        'notes': 'Test Notes',
        'start_date': '2024-04-04',
        'end_date': '2024-04-10',
        'location': 'Test Location'
    }
    response = client.post(reverse('add_inspection_and_quarantine'), data=data)
    assert response.status_code == 302

@pytest.mark.fifth
def test_show_inspections_and_quarantines(client):
    inspection = VeterinaryInspection.objects.create(inspection_date='2024-04-04', veterinarian='Test Vet', results='Test Results')
    quarantine = Quarantine.objects.create(start_date='2024-04-04', end_date='2024-04-10', location='Test Location')

    response = client.get(reverse('show_inspections_and_quarantines'))
    assert response.status_code == 200
    assert inspection in response.context['inspections']
    assert quarantine in response.context['quarantines']


@pytest.mark.sixth
def test_add_asf_incident_post(client):

    user = User.objects.create_user(username='test_user', password='password123')

    data = {
        'detection_date': '2024-04-04',
        'location': 'Test Location',
        'infected_count': 10,
        'veterinary_inspections': 'Test Inspection',
        'quarantines': 'Test Quarantine'
    }

    client.login(username='test_user', password='password123')

    response = client.post(reverse('add_asf_incident'), data=data)
    assert response.status_code == 302
    assert ASFIncident.objects.filter(location="Test Location").exists()


@pytest.mark.seventh
def test_add_additional_info_get(client):
    response = client.get(reverse('add_additional_info'))
    assert response.status_code == 200
