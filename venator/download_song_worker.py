import os 
import requests 
from redis import Redis
from multiprocessing import Process
from rq import Queue,Worker,Connection
from song_downloader import SongDownloader
from config.download_song_queue import download_song_queue,redis_conn

workers = int(os.getenv("WORKERS"))

def worker_proc(download_song_queue,worker_id):
    global songDownloader_ins # that way it's set in the global context so we don't have to re-init selenium every time we get a request
    # see https://python-rq-docs-cn.readthedocs.io/en/latest/workers.html#inside-the-worker
    songDownloader_ins = SongDownloader(worker_id)
    with Connection(connection=redis_conn):
        worker = Worker(download_song_queue).work(logging_level='info')

def download_song(song_url):
    songDownloader_ins.download_song(song_url)
    
for w in range(workers):
    p = Process(
        target=worker_proc,
        args=(download_song_queue,'worker_'+str(w))
    )

    p.start()
print("Spawning {0} RQ workers".format(workers))
