from django.contrib import admin

from apps.resume.models import (
    CourseModel,
    EducationModel,
    LanguageModel,
    LinkModel,
    ProjectModel,
    ResumeModel,
    ResumeTemplateModel,
    SkillModel,
    WorkExperienceModel,
)

admin.site.register(
    [
        ResumeTemplateModel,
        ResumeModel,
        WorkExperienceModel,
        ProjectModel,
        EducationModel,
        CourseModel,
        LinkModel,
        SkillModel,
        LanguageModel,
    ]
)
