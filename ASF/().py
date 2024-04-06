# coding: utf-8
from Tracer_app.models import ASFIncident, VeterinaryInspection, Quarantine, EpidemiologicalReport, BreedingFarm, MedicalResource

VeterinaryInspection.objects.create(
    inspection_date='2024-04-06',
    veterinarian="Dr. John Doe",
    results="All animals are healthy.",
    notes="No issues found during the inspection."
)

Quarantine.objects.create(
    start_date='2024-04-08',
    end_date='2024-04-20',
    location="Farm C"
)
