# Generated by Django 5.0.3 on 2024-03-27 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tracer_app', '0006_remove_asfincident_quarantines_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asfincident',
            name='veterinary_inspections',
        ),
    ]