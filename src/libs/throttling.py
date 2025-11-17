from rest_framework.throttling import SimpleRateThrottle


class CustomUserRateThrottle(SimpleRateThrottle):
    scope = "user_scope"

    def get_cache_key(self, request, view):
        user = getattr(request, "user", None)
        token = getattr(request, "auth", None)

        if user and token:
            ident = f"{user.pk}:{token}"
            return self.cache_format % {"scope": self.scope, "ident": ident}

        return self.get_ident(request)


class CustomAnonRateThrottle(SimpleRateThrottle):
    scope = "anon_scope"

    def get_cache_key(self, request, view):
        if request.user:
            return None

        return self.cache_format % {
            "scope": self.scope,
            "ident": self.get_ident(request),
        }
