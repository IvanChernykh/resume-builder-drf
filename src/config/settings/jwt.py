import os
from datetime import timedelta

JWT_SETTINGS = {
    "algorithm": os.getenv("JWT_ALG"),
    "access_exp": timedelta(minutes=10),
    "refresh_exp": timedelta(days=7),
    "access_secret": os.getenv("JWT_ACCESS_SECRET"),
    "refresh_secret": os.getenv("JWT_REFRESH_SECRET"),
}
