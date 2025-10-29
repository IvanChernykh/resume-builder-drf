import os

import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB_JWT = int(os.getenv("REDIS_DB_JWT", 1))

REDIS_JWT = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_JWT, decode_responses=True
)
