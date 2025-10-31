from datetime import timedelta
from uuid import uuid4

from django.db import models
from django.utils import timezone

from apps.users.models import UserModel


class EmailConfirmationTokenModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    user: "models.ForeignKey[UserModel]" = models.ForeignKey(
        "users.UserModel", on_delete=models.CASCADE, related_name="+"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self) -> bool:
        epiry_time = self.created_at + timedelta(minutes=20)
        return timezone.now() > epiry_time

    def belongs_to_user(self, user: UserModel) -> bool:
        return self.user.id == user.id
