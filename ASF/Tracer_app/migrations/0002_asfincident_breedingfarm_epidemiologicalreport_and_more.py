# Generated by Django 5.0.3 on 2024-03-26 16:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracer_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ASFIncident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detection_date', models.DateField()),
                ('location', models.CharField(max_length=100)),
                ('infected_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BreedingFarm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('pig_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EpidemiologicalReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateField()),
                ('description', models.TextField()),
                ('preventive_measures', models.TextField()),
                ('asf_incidents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tracer_app.asfincident')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Quarantine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VeterinaryInspection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inspection_date', models.DateField()),
                ('veterinarian', models.CharField(max_length=100)),
                ('results', models.TextField()),
                ('notes', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Report',
        ),
        migrations.AddField(
            model_name='asfincident',
            name='quarantines',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tracer_app.quarantine'),
        ),
        migrations.AddField(
            model_name='asfincident',
            name='veterinary_inspections',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tracer_app.veterinaryinspection'),
        ),
    ]
