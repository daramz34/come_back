import redis
import json
from Blogging_api.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_cache(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key: str, value: dict, expire: int = 60):
    redis_client.setex(key, expire, json.dumps(value))

def delete_cache(key: str):
    redis_client.delete(key)