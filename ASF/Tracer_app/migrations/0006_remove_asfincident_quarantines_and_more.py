# Generated by Django 5.0.3 on 2024-03-27 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tracer_app', '0005_remove_asfincident_medical_resources'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asfincident',
            name='quarantines',
        ),
        migrations.RemoveField(
            model_name='epidemiologicalreport',
            name='asf_incidents',
        ),
    ]
