from django.urls import path

from apps.resume.views.resume_template_views import resume_template_view
from apps.resume.views.resume_views import resume_view

app_name = "apps.resume"

urlpatterns = [
    path("resume/template/", resume_template_view, name="resume_template"),
    path("resume/", resume_view, name="resume"),
]
