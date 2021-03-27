from multiprocessing import Process
from rq import Queue,Worker,Connection
from config.redis_conn import redis_conn



download_song_queue = Queue(
    name="download_song_queue",
    connection=redis_conn,
)
