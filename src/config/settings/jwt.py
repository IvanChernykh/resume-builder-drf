import os
from datetime import timedelta

JWT_REFRESH_TTL_DAYS = int(os.getenv("JWT_REFRESH_TTL_DAYS", 7))
JWT_REFRESH_TTL_SECONDS = JWT_REFRESH_TTL_DAYS * 24 * 60 * 60

JWT_SETTINGS = {
    "algorithm": os.getenv("JWT_ALG"),
    "access_exp": timedelta(minutes=10),
    "refresh_exp": timedelta(days=JWT_REFRESH_TTL_DAYS),
    "access_secret": os.getenv("JWT_ACCESS_SECRET"),
    "refresh_secret": os.getenv("JWT_REFRESH_SECRET"),
}
