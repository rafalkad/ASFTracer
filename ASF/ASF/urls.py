"""
URL configuration for ASF project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from Tracer_app.views import asf_incident_list, AddASFIncident, AddAdditionalInfo, AddInspectionAndQuarantine, ShowInspectionsAndQuarantines, notify_mailchimp_about_asf_incident

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('asf_incidents/', asf_incident_list, name='asf_incident_list'),
    path('add_inspection_and_quarantine/', AddInspectionAndQuarantine.as_view(), name='add_inspection_and_quarantine'),
    path('show_inspections_and_quarantines/', ShowInspectionsAndQuarantines.as_view(),
         name='show_inspections_and_quarantines'),
    path('add_asf_incident/', AddASFIncident.as_view(), name='add_asf_incident'),
    path('add_additional_info/', AddAdditionalInfo.as_view(), name='add_additional_info'),
    path('notify_mailchimp/', notify_mailchimp_about_asf_incident, name='notify_mailchimp'),

]