from dotenv import load_dotenv
# if an ENV var is set don't override it
load_dotenv(verbose=True, dotenv_path="./config/.env",override=False)

import os
import json
import time
from config.redis_conn import redis_conn_sub
from download_song_worker import download_song
from config.rabbit_channel import channel,connection
from config.download_song_queue import download_song_queue

# remove the '.inuse' from all cookie jars from the prev. session
inuse_cookie_jars = [cookie_jar for cookie_jar in os.listdir('config/secrets') if "inuse" in cookie_jar]
[os.rename("config/secrets/"+cookie_jar,"config/secrets/"+cookie_jar.replace('.inuse','')) for cookie_jar in inuse_cookie_jars]


def enqueue_request(channel, method_frame, header_frame, body):
    requestMsg = json.loads(body)
    print("enqueuing "+str(requestMsg))
    # add it to the queue here
    download_song_queue.enqueue(download_song,requestMsg['song_url'])
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    return

channel.basic_consume('download_requests', enqueue_request)

while True:
    try:
        print("VENATOR service up and running")
        channel.start_consuming()
    except Exception as e:
        print(e)
        print("stoping VENATOR download_requests consumer")
        channel.stop_consuming()
        connection.close()
