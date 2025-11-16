from django.urls import path

from apps.resume.views.resume_section_views import resume_section_view
from apps.resume.views.resume_template_views import resume_template_view
from apps.resume.views.resume_views import resume_detail_view, resume_view

app_name = "apps.resume"

urlpatterns = [
    path("resume/template/", resume_template_view, name="resume_template"),
    path(
        "resume/<uuid:resume_id>/sections/", resume_section_view, name="resume_section"
    ),
    path("resume/<uuid:resume_id>/", resume_detail_view, name="resume_detail"),
    path("resume/", resume_view, name="resume"),
]
