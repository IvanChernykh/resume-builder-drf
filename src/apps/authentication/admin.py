from django.contrib import admin

from apps.authentication.models import EmailConfirmationTokenModel

admin.site.register(EmailConfirmationTokenModel)
