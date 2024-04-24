# Generated by Django 5.0.3 on 2024-03-27 19:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracer_app', '0008_epidemiologicalreport_asf_incidents'),
    ]

    operations = [
        migrations.AddField(
            model_name='asfincident',
            name='quarantines',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Tracer_app.quarantine'),
        ),
        migrations.AddField(
            model_name='asfincident',
            name='veterinary_inspections',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Tracer_app.veterinaryinspection'),
        ),
    ]