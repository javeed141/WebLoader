import time
import logging
from collections import defaultdict
from fastapi import Request
from fastapi.responses import JSONResponse

from app.redis_client import redis_client

logger = logging.getLogger(__name__)

MAX_ALLOWED_REQ = 4
MAX_TIME = 30  # seconds

# In-memory fallback rate limiter tracking: { client_ip: [timestamps] }
_in_memory_store: dict[str, list[float]] = defaultdict(list)


# def _check_in_memory_rate_limit(client_ip: str) -> bool:
#     """Fallback rate limiting in memory if Redis is unavailable.
#     Returns True if rate limit is exceeded, False otherwise.
#     """
#     now = time.time()
#     timestamps = _in_memory_store[client_ip]
#     # Filter out timestamps outside the window
#     valid_timestamps = [ts for ts in timestamps if now - ts < MAX_TIME]
#     _in_memory_store[client_ip] = valid_timestamps

#     if len(valid_timestamps) >= MAX_ALLOWED_REQ:
#         return True

#     _in_memory_store[client_ip].append(now)
#     return False


async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    key = f"rate_limit:{client_ip}"

    is_limited = False

    if redis_client is not None:
        try:
            request_count = await redis_client.incr(key)
            if request_count == 1:
                await redis_client.expire(key, MAX_TIME)

            if request_count > MAX_ALLOWED_REQ:
                is_limited = True
        except Exception as exc:
            logger.warning("Redis error during rate limiting, falling back to in-memory: %s", exc)
            is_limited = _check_in_memory_rate_limit(client_ip)
    # else:
    #     is_limited = _check_in_memory_rate_limit(client_ip)

    if is_limited:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please try again later."}
        )

    response = await call_next(request)
    return response