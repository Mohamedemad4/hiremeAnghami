from dotenv import load_dotenv
# if an ENV var is set don't override it
load_dotenv(verbose=True, dotenv_path="./config/.env",override=False)

import os
import json
import time
from config.redis_conn import redis_conn_sub
from download_song_worker import download_song
from config.download_song_queue import download_song_queue

print("Subcribing to download_requests")
redis_conn_sub.subscribe('download_requests')

# remove the '.inuse' from all cookie jars from the prev. session
inuse_cookie_jars = [cookie_jar for cookie_jar in os.listdir('config/secrets') if "inuse" in cookie_jar]
[os.rename("config/secrets/"+cookie_jar,"config/secrets/"+cookie_jar.replace('.inuse','')) for cookie_jar in inuse_cookie_jars]

while True:
    msg = redis_conn_sub.get_message()
    if msg:
        if msg['data']!=1 and msg['data']:
            requestMsg = json.loads(msg['data'])
            print("enqueuing "+str(requestMsg))
            # add it to the queue here
            download_song_queue.enqueue(download_song,requestMsg['song_url'])
    time.sleep(.5)

print("VENATOR service up and running")