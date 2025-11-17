from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class DoubleSubmitCSRF(BasePermission):

    def has_permission(self, request, view):
        cookie_token = request.COOKIES.get("csrf_token")
        header_token = request.headers.get("X-CSRFToken")

        if not cookie_token or not header_token:
            raise PermissionDenied("csrf token is missing or invalid")

        if cookie_token != header_token:
            raise PermissionDenied("csrf token is missing or invalid")

        return True
