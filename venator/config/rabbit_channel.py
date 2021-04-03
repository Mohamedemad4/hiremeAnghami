import os
import pika

credentials = pika.PlainCredentials(
    os.getenv("RABBIT_USER"),
    os.getenv("RABBIT_PASS")    
)

conn_params = pika.ConnectionParameters(os.getenv("RABBIT_HOST"),
                                       os.getenv("RABBIT_PORT"),
                                       '/',
                                       credentials)

#  we shouldn't share connection objs across "threads" or different workers in our case
# https://pika.readthedocs.io/en/stable/faq.html
# this connection obj is just used to define topology and then consume download_requests
# later each worker defines their own connection and channel objects
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()
channel.queue_declare(queue='download_requests')
channel.queue_declare(queue='downloaded_songs')
