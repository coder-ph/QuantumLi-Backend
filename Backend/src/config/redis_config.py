import logging
import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
_redis_client = None

def init_redis():
    global _redis_client
    try:
        if REDIS_URL:
            _redis_client = redis.StrictRedis.from_url(
                REDIS_URL,
                decode_responses=True,
                socket_timeout=5,
                retry_on_timeout=True
            )
            logging.info("Redis connection established via URL.")
        else:
            logging.warning("REDIS_URL environment variable not set. Falling back to manual configuration.")
            _redis_client = redis.StrictRedis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                username=os.getenv("REDIS_USER", "default"),
                password=os.getenv("REDIS_PASSWORD"),
                # db=int(os.getenv("REDIS_DB", 0)),
                decode_responses=True,
                socket_timeout=5,
                retry_on_timeout=True
            )
            logging.info("Redis connection established via manual configuration.")

        _redis_client.ping()
        logging.info("Redis connection successful.")
        return _redis_client

    except Exception as e:
        logging.error(f"Redis connection failed: {str(e)}")
        raise

def get_redis_client():
    global _redis_client
    if _redis_client is None:
        _redis_client = init_redis()
    return _redis_client

def init_pubsub():
    redis_client = get_redis_client()
    return redis_client.pubsub()
