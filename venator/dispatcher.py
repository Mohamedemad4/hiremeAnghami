from dotenv import load_dotenv
# if an ENV var is set don't override it
load_dotenv(verbose=True, dotenv_path="./config/.env",override=False)

import os
import json
import time
from config.redis_conn import redis_conn_sub
from song_downloader import SongDownloader

print("VENATOR service up and running")
print("Subcribing to download_requests")

redis_conn_sub.subscribe('download_requests')
SongDownloader_ins = SongDownloader() # todo start N-instances and keep them running and make it configurable 

while True:
    msg = redis_conn_sub.get_message()
    if msg:
        if msg['data']!=1 and msg['data']:
            requestMsg = json.loads(msg['data'])
            print("PROCESSING "+str(requestMsg))
            # add it to the queue here
            SongDownloader_ins.download_song(requestMsg['song_url'])

    time.sleep(.5)