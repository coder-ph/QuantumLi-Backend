from flask_jwt_extended import get_jti
from datetime import timedelta
from src.config.redis_config import init_redis 
from src.utils.logger import logger
from src.config.redis_config import get_redis_client
import json

REVOCATION_KEY_PREFIX = "revoked_tokens"


def revoke_token(token, expires_in):
   
    try:
        if not token or expires_in <= 0:
            raise ValueError("Invalid token or expiration time.")

        jti = get_jti(token)
        key = f"{REVOCATION_KEY_PREFIX}:{jti}"
        init_redis.redis_client.setex(key, timedelta(seconds=expires_in), "revoked")
        logger.info(f"Token revoked | jti: {jti} | expires_in: {expires_in}s")

        return True
    except Exception as e:
        logger.exception(f"Failed to revoke token | Reason: {str(e)}")
        return False


def is_token_revoked(jti):
    try:
        if not jti:
            logger.warning("JTI check called with None or empty value.")
            return True

        key = f"{REVOCATION_KEY_PREFIX}:{jti}"
        redis_client = get_redis_client()  
        is_revoked = redis_client.exists(key) == 1

        logger.debug(f"{' Revoked' if is_revoked else ' Valid'} token | jti: {jti}")
        return is_revoked
    except Exception as e:
        logger.exception(f" Error checking if token is revoked | jti: {jti} | Reason: {str(e)}")
        return True


def clean_expired_revoked_tokens():

    try:
        cleaned = 0
        pattern = f"{REVOCATION_KEY_PREFIX}:*"
        for key in init_redis.redis_client.scan_iter(match=pattern, count=100):
            ttl = init_redis.redis_client.ttl(key)
            if ttl == -1:  # No expiration set
                init_redis.redis_client.delete(key)
                logger.info(f" Cleaned stale revoked token: {key}")
                cleaned += 1
        logger.info(f" Redis cleanup complete | {cleaned} keys deleted.")
        return cleaned
    except Exception as e:
        logger.exception(f"Failed to clean expired revoked tokens | Reason: {str(e)}")
        return 0
