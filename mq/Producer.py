import pika
from config import *

class Producer:
    def __init__(self):
        self.exchange = rmq_exchange
        credentials = pika.PlainCredentials(rmq_user, rmq_pw)
        connection = pika.BlockingConnection(pika.ConnectionParameters(rmq_ip, rmq_port, rmq_vhost, credentials))
        self.channel = connection.channel()