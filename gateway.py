from threading import Thread

import json
import eel




class Gateway:
    def __init__(self, freq, producer, consumer):
        self.freq = freq
        self.producer = producer
        self.consumer = consumer
        self.consumer.callback = self.receiveMessage

        self.producer.channel.exchange_declare(exchange=self.producer.exchange, exchange_type="topic", durable=True,
                                               auto_delete=False)

    def getRoutingKey(self):
        return "gateway"


    def send(self, message, routing_key):
        self.producer.channel.basic_publish(exchange=self.producer.exchange, routing_key=routing_key, body=message)


    def getValue(self):
        eel.setText('gateway', self.status)

    def receiveMessage(ch, method, properties, k, body):
        resp = json.loads(body.decode('utf-8'))
        if resp['function'] == 'execute':
            # print(str(resp['value']['status']), " :::: ", ch.getRoutingKey() + "." + resp['value']['actuator'])
            ch.send(str(resp['value']['status']), ch.getRoutingKey() + "." + resp['value']['actuator'])
        else:
            ch.send(json.dumps(resp), ch.getRoutingKey() + "." + "context")


    def start(self):
        Thread(target=self.consumer.start, args=[]).start()

