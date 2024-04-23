from django.db import models


# Create your models here.


class ASFIncident(models.Model):
    detection_date = models.DateField()
    location = models.CharField(max_length=100)
    infected_count = models.IntegerField()
    veterinary_inspections = models.ForeignKey('VeterinaryInspection', on_delete=models.CASCADE, null=True, default=None)
    quarantines = models.ForeignKey('Quarantine', on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"ASFIncident ({self.detection_date}: {self.location})"


class VeterinaryInspection(models.Model):
    inspection_date = models.DateField()
    veterinarian = models.CharField(max_length=100)
    results = models.TextField()
    notes = models.TextField()

    def __str__(self):
        return f"Veterinary Inspection ({self.id}: {self.inspection_date})"


class Quarantine(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"Quarantine ({self.id}: {self.location})"


class EpidemiologicalReport(models.Model):
    report_date = models.DateField()
    description = models.TextField()
    preventive_measures = models.TextField()
    asf_incidents = models.ForeignKey('ASFIncident', on_delete=models.CASCADE, default=None)


class BreedingFarm(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    pig_count = models.IntegerField()
    asf_incidents = models.ManyToManyField('ASFIncident', related_name='breeding_farms', blank=True)


class MedicalResource(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    description = models.TextField()
    asf_incidents = models.ManyToManyField('ASFIncident', related_name='medical_resources', blank=True)
