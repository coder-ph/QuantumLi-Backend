import logging
from flask import current_app
import redis


def init_redis():
    try:
        redis_host = current_app.config['REDIS_HOST']
        redis_port = current_app.config["REDIS_PORT"]
        redis_db = current_app.config["REDIS_DB"]
        redis_client = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True,
            socket_timeout=5,                               
            retry_on_timeout=True, 
                )
        redis_client.ping()
        print("redis conn established")
        return redis_client
    
    except Exception as e:
        logging.error(f"Redis connection failed: {str(e)}")
        raise
    
def init_pubsub():
    redis_client = init_redis()
    pubsub = redis_client.pubsub()
    return pubsub