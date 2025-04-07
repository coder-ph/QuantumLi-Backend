import redis
import time
from flask import request
from src.handlers.repositories.auth_repository import get_user_by_username
from src.services_layer.auth.auth_service import generate_tokens, verify_password
from src.utils.logger import logger
from src.config.redis_config import redis_client
import hashlib
import json

THROTTLE_KEY = "login_attempts:"
BLOCK_DURATION = 300  
MAX_ATTEMPTS = 5


def get_device_fingerprint():
    """
    Generate a simple device fingerprint using user-agent, IP, and accepted headers.
    """
    user_agent = request.headers.get('User-Agent', '')
    ip = request.remote_addr or ''
    accept = request.headers.get('Accept', '')
    raw_fingerprint = f"{user_agent}:{ip}:{accept}"
    fingerprint = hashlib.sha256(raw_fingerprint.encode()).hexdigest()
    return fingerprint


def track_login_attempt(username):
    ip = request.remote_addr
    key = f"{THROTTLE_KEY}{username}:{ip}"
    attempts = redis_client.get(key)

    if attempts and int(attempts) >= MAX_ATTEMPTS:
        logger.warning(f"Login blocked for user {username} from IP {ip}")
        return False

    redis_client.incr(key)
    redis_client.expire(key, BLOCK_DURATION)
    return True


def reset_login_attempts(username):
    ip = request.remote_addr
    key = f"{THROTTLE_KEY}{username}:{ip}"
    redis_client.delete(key)


def login_user(username, password):
    user = get_user_by_username(username)

    if not user:
        return None, "Invalid credentials"

    if not track_login_attempt(username):
        return None, "Too many login attempts. Please wait a few minutes."

    if not verify_password(user.password_hash, password):
        return None, "Invalid credentials"

    reset_login_attempts(username)

    fingerprint = get_device_fingerprint()

    
    session_id = f"user_session:{user.id}:{int(time.time())}"
    session_data = {
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent", ""),
        "fingerprint": fingerprint,
        "login_time": int(time.time())
    }
    redis_client.set(session_id, json.dumps(session_data), ex=86400)  

    roles = [user.role]  
    access_token, refresh_token = generate_tokens(user, roles=roles)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        },
        "session": session_data
    }, None
