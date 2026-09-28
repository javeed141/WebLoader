import os
import logging
import redis.asyncio as redis

logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "sound-hearty-dope-77411.db.redis.io")
REDIS_PORT = int(os.getenv("REDIS_PORT", "13998"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

redis_client = None

if REDIS_PASSWORD:
    try:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True,
            username="default",
            password=REDIS_PASSWORD,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
    except Exception as e:
        logger.warning(f"Failed to initialize Redis client: {e}")
        redis_client = None
else:
    logger.warning("REDIS_PASSWORD environment variable not set. Redis client will be disabled.")
