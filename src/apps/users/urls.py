from django.urls import path

from apps.users.views import me

app_name = "apps.users"

urlpatterns = [path("me/", me, name="me")]
urlpatterns = [path("me/", me, name="me")]
