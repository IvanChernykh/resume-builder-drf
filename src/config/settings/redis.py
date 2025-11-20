import os

import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB_JWT = int(os.getenv("REDIS_DB_JWT", 1))
REDIS_DB_EMAIL_TOKEN = int(os.getenv("REDIS_DB_EMAIL_TOKEN", 2))
REDIS_DB_PW_RESET_TOKEN = int(os.getenv("REDIS_DB_EMAIL_TOKEN", 3))

REDIS_JWT = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_JWT, decode_responses=True
)

REDIS_EMAIL_TOKEN = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_EMAIL_TOKEN, decode_responses=True
)

REDIS_PW_RESET_TOEKN = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_PW_RESET_TOKEN, decode_responses=True
)
