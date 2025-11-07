from django.urls import path

from apps.resume.views.resume_template_views import get_all_resume_templates
from apps.resume.views.resume_views import create_resume

app_name = "apps.resume"

urlpatterns = [
    path("resume/template/", get_all_resume_templates, name="get_resume_templates"),
    path("resume/", create_resume, name="create_resume"),
]
