from rest_framework import serializers

from apps.resume.models import (
    CourseModel,
    EducationModel,
    LanguageModel,
    LinkModel,
    ProjectModel,
    SkillModel,
    WorkExperienceModel,
)


# ---------------------------------------------------------------------
# work experience
# ---------------------------------------------------------------------
class WorkExperienceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperienceModel
        fields = "__all__"


class WorkExperienceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperienceModel
        fields = [
            "job_title",
            "employer",
            "city",
            "start_end_date",
            "description",
            "sort_order",
        ]


class WorkExperienceUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = WorkExperienceModel
        fields = [
            "id",
            "job_title",
            "employer",
            "city",
            "start_end_date",
            "description",
            "sort_order",
        ]


# ---------------------------------------------------------------------
# education
# ---------------------------------------------------------------------
class EducationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationModel
        fields = "__all__"


class EducationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationModel
        fields = [
            "school",
            "degree",
            "city",
            "start_end_date",
            "description",
            "sort_order",
        ]


class EducationUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = EducationModel
        fields = [
            "id",
            "school",
            "degree",
            "city",
            "start_end_date",
            "description",
            "sort_order",
        ]


# ---------------------------------------------------------------------
# project
# ---------------------------------------------------------------------
class ProjectGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = "__all__"


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = ["title", "link", "link_to_repo", "description", "sort_order"]


class ProjectUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = ProjectModel
        fields = ["id", "title", "link", "link_to_repo", "description", "sort_order"]


# ---------------------------------------------------------------------
# skill
# ---------------------------------------------------------------------
class SkillGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillModel
        fields = "__all__"


class SkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillModel
        fields = ["title", "level", "sort_order"]


class SkillUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = SkillModel
        fields = ["id", "title", "level", "sort_order"]


# ---------------------------------------------------------------------
# course
# ---------------------------------------------------------------------
class CourseGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = "__all__"


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = ["course", "institution", "start_end_date", "sort_order"]


class CourseUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = CourseModel
        fields = ["id", "course", "institution", "start_end_date", "sort_order"]


# ---------------------------------------------------------------------
# link
# ---------------------------------------------------------------------
class LinkGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkModel
        fields = "__all__"


class LinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkModel
        fields = ["title", "link", "sort_order"]


class LinkUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = LinkModel
        fields = ["id", "title", "link", "sort_order"]


# ---------------------------------------------------------------------
# language
# ---------------------------------------------------------------------
class LanguageGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageModel
        fields = "__all__"


class LanguageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageModel
        fields = ["language", "level", "sort_order"]


class LanguageUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = LanguageModel
        fields = ["id", "language", "level", "sort_order"]


# ---------------------------------------------------------------------
# crud sections
# ---------------------------------------------------------------------


class CreateSectionsSerializer(serializers.Serializer):
    work_experience = WorkExperienceCreateSerializer(many=True, required=False)
    education = EducationCreateSerializer(many=True, required=False)
    projects = ProjectCreateSerializer(many=True, required=False)
    skills = SkillCreateSerializer(many=True, required=False)
    courses = CourseCreateSerializer(many=True, required=False)
    links = LinkCreateSerializer(many=True, required=False)
    languages = LanguageCreateSerializer(many=True, required=False)


class UpdateSectionsSerializer(serializers.Serializer):
    work_experience = WorkExperienceUpdateSerializer(many=True, required=False)
    education = EducationUpdateSerializer(many=True, required=False)
    projects = ProjectUpdateSerializer(many=True, required=False)
    skills = SkillUpdateSerializer(many=True, required=False)
    courses = CourseUpdateSerializer(many=True, required=False)
    links = LinkUpdateSerializer(many=True, required=False)
    languages = LanguageUpdateSerializer(many=True, required=False)


class DeleteSectionsSerializer(serializers.Serializer):
    work_experience = serializers.ListField(
        child=serializers.UUIDField(), required=False
    )
    education = serializers.ListField(child=serializers.UUIDField(), required=False)
    projects = serializers.ListField(child=serializers.UUIDField(), required=False)
    links = serializers.ListField(child=serializers.UUIDField(), required=False)
    skills = serializers.ListField(child=serializers.UUIDField(), required=False)
    languages = serializers.ListField(child=serializers.UUIDField(), required=False)
    courses = serializers.ListField(child=serializers.UUIDField(), required=False)


class CopySectionSerializer(serializers.Serializer):
    target_resume = serializers.UUIDField()
    work_experience = serializers.UUIDField(required=False)
    education = serializers.UUIDField(required=False)
    projects = serializers.UUIDField(required=False)
    links = serializers.UUIDField(required=False)
    skills = serializers.UUIDField(required=False)
    languages = serializers.UUIDField(required=False)
    courses = serializers.UUIDField(required=False)
