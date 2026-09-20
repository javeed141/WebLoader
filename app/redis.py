"""Basic connection example.
"""
import os
import redis.asyncio as redis

redis_client = redis.Redis(
    host='sound-hearty-dope-77411.db.redis.io',
    port=13998,
    decode_responses=True,
    username="default",
    password=os.environ["REDIS_PASSWORD"],
)

success = redis_client.set('foo', 'bar')
# True

result = redis_client.get('foo')
print(result)
# >>> bar

