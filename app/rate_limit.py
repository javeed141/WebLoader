from fastapi import Request
from fastapi.responses import JSONResponse

from app.redis import redis_client


MAX_ALLOWED_REQ = 4
MAX_TIME = 30


async def rate_limit_middleware(request: Request, call_next):

    client_ip = request.client.host

    key = f"rate_limit:{client_ip}"

    request_count = await redis_client.incr(key)

    if request_count == 1:
        await redis_client.expire(key, MAX_TIME)

    if request_count > MAX_ALLOWED_REQ:
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Too many requests"
            }
        )

    response = await call_next(request)

    return response