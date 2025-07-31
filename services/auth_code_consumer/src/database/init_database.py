import redis
from redis import Redis
from src.config import get_settings

settings = get_settings()

redis_client = Redis(host=settings.redis_connection_url, port=settings.redis_port, db=0)

def initiate_database() -> Redis:
    return redis_client


