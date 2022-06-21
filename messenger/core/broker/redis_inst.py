import aioredis

redis = aioredis.Redis.from_url(
    "redis://127.0.0.1:6379", max_connections=10, decode_responses=True
)