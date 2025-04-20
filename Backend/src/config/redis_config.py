import logging
from flask import current_app
import redis


def init_redis():
    try:
        redis_host = current_app.config['REDIS_HOST']
        redis_port = current_app.config["REDIS_PORT"]
        redis_db = current_app.config["REDIS_DB"]
        redis_password = current_app.config["REDIS_PASSWORD"]
        redis_client = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password,
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

_redis_client = None

def get_redis_client():
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.StrictRedis(
                host=current_app.config['REDIS_HOST'],
                port=current_app.config['REDIS_PORT'],
                db=current_app.config['REDIS_DB'],
                decode_responses=True,
                socket_timeout=5,
                retry_on_timeout=True,
            )
            _redis_client.ping()
            logging.info("Redis connection established")
        except Exception as e:
            logging.error(f"Redis connection failed: {str(e)}")
            raise
    return _redis_client

def init_pubsub():
    redis_client = init_redis()
    pubsub = redis_client.pubsub()
    return pubsub