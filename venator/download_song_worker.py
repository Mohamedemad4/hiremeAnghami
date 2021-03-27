import os 
import requests 
from redis import Redis
from multiprocessing import Process
from rq import Queue,Worker,Connection
from config.containers import lxd_client
from config.download_song_queue import download_song_queue,redis_conn

def worker_proc(download_song_queue):
    with Connection(connection=redis_conn):
        worker = Worker(download_song_queue).work(logging_level='info')

p = Process(
    target=worker_proc,
    args=download_song_queue,
    daemon=False # can't have children if you are a demon 
)

p.start()