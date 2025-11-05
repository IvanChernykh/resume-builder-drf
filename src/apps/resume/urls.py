from django.urls import path

from apps.resume.views.resume_template_views import get_all_resume_templates

app_name = "apps.resume"

urlpatterns = [
    path("resume/template/", get_all_resume_templates, name="get_resume_templates")
]
