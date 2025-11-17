from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from utils.constants.cookies import COOKIE_CSRF_TOKEN
from utils.constants.headers import HEADER_CSRF_TOKEN


class DoubleSubmitCSRF(BasePermission):

    def has_permission(self, request, view):
        cookie_token = request.COOKIES.get(COOKIE_CSRF_TOKEN)
        header_token = request.headers.get(HEADER_CSRF_TOKEN)

        if not cookie_token or not header_token:
            raise PermissionDenied("csrf token is missing or invalid")

        if cookie_token != header_token:
            raise PermissionDenied("csrf token is missing or invalid")

        return True
