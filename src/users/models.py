from uuid import uuid4

from django.db import models


class UserModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=128)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
