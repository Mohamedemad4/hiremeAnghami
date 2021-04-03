import os
import pika

conn_params = pika.URLParameters(os.getenv("AMQP_URI"))

#  we shouldn't share connection objs across "threads" or different workers in our case
# https://pika.readthedocs.io/en/stable/faq.html
# this connection obj is just used to define topology and then consume download_requests
# later each worker defines their own connection and channel objects
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()
channel.queue_declare(queue='download_requests')
channel.queue_declare(queue='downloaded_songs')
