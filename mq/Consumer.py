from threading import Thread
from config import *
import pika

class Consumer:
    def __init__(self, queue, routingKey):
        self.queue = queue
        self.routingKey = routingKey
        self.callback = self.receiveMessage

        credentials = pika.PlainCredentials(rmq_user, rmq_pw)
        connection = pika.BlockingConnection(pika.ConnectionParameters(rmq_ip, rmq_port, rmq_vhost, credentials))
        self.channel = connection.channel()

    def receiveMessage(ch, method, properties, k, body):
        print('Received: {}'.format(body))

    def start(self):
        self.channel.exchange_declare(exchange=rmq_exchange, exchange_type='topic', durable=True, auto_delete=False)
        self.channel.queue_declare(queue=self.queue)
        self.channel.queue_bind(queue=self.queue, exchange=rmq_exchange, routing_key=self.routingKey)

        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
        print('Waiting for messages')
        self.channel.start_consuming()
