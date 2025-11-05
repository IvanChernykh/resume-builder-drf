from uuid import uuid4

from django.core.validators import MaxValueValidator
from django.db import models

from apps.users.models import UserModel


class ResumeTemplateModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=128, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ResumeModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    resume_name = models.CharField(max_length=64)

    job_title = models.CharField(max_length=64, blank=True)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    email = models.EmailField(max_length=64, blank=True)
    phone = models.CharField(max_length=25, blank=True)
    country = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64, blank=True)
    summary = models.CharField(max_length=500, blank=True)

    template = models.ForeignKey(
        ResumeTemplateModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name="resumes",
        db_column="template_id",
    )

    owner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="resumes",
        db_column="owner_id",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.resume_name


class WorkExperienceModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    job_title = models.CharField(max_length=128, blank=True)
    employer = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    start_end_date = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=500, blank=True)
    sort_order = models.PositiveIntegerField()

    resume = models.ForeignKey(
        ResumeModel,
        on_delete=models.CASCADE,
        related_name="work_experience",
        db_column="resume_id",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EducationModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    school = models.CharField(max_length=128, blank=True)
    degree = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    start_end_date = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=500, blank=True)
    sort_order = models.PositiveIntegerField()

    resume = models.ForeignKey(
        ResumeModel,
        on_delete=models.CASCADE,
        related_name="education",
        db_column="resume_id",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProjectModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    title = models.CharField(max_length=128, blank=True)
    link = models.URLField(max_length=1000, blank=True)
    link_to_repo = models.URLField(max_length=1000, blank=True)
    description = models.CharField(max_length=500, blank=True)
    sort_order = models.PositiveIntegerField()

    resume = models.ForeignKey(
        ResumeModel,
        on_delete=models.CASCADE,
        related_name="projects",
        db_column="resume_id",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SkillModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    title = models.CharField(max_length=128, blank=True)
    level = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    sort_order = models.PositiveIntegerField()

    resume = models.ForeignKey(
        ResumeModel,
        on_delete=models.CASCADE,
        related_name="skills",
        db_column="resume_id",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CourseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    course = models.CharField(max_length=128, blank=True)
    institution = models.CharField(max_length=128, blank=True)
    start_end_date = models.CharField(max_length=128, blank=True)
    sort_order = models.PositiveIntegerField()

    resume = models.ForeignKey(
        ResumeModel,
        on_delete=models.CASCADE,
        related_name="courses",
        db_column="resume_id",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LinkModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    title = models.CharField(max_length=128, blank=True)
    link = models.URLField(max_length=1000, blank=True)
    sort_order = models.PositiveIntegerField()

    resume = models.ForeignKey(
        ResumeModel,
        on_delete=models.CASCADE,
        related_name="links",
        db_column="resume_id",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LanguageModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    language = models.CharField(max_length=128, blank=True)
    level = models.CharField(max_length=128, blank=True)
    sort_order = models.PositiveIntegerField()

    resume = models.ForeignKey(
        ResumeModel,
        on_delete=models.CASCADE,
        related_name="languages",
        db_column="resume_id",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
