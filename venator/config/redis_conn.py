import os 
from redis import Redis

redis_conn = Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    db=os.getenv('REDIS_DB')
)

redis_conn_sub = Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    db=os.getenv('REDIS_DB')
).pubsub()

