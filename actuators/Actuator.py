from threading import Thread
import time

import eel

from mq.Producer import Producer


class Actuator:
    def __init__(self, typ, id, location, freq, consumer):
        self.typ = typ
        self.id = id
        self.location = location
        self.freq = freq
        self.producer = Producer()
        self.consumer = consumer
        self.value = 0
        self.envEffect = dict()

        self.function = 'actuator'

    def getRoutingKey(self):
        return self.location.building+"."+self.location.floor+"."+self.location.room+".actuator."+self.typ+"."+self.id

    def send(self):
        self.producer.channel.exchange_declare(exchange=self.producer.exchange, exchange_type="topic", durable=True, auto_delete=False)
        while True:
            message = self.getMessage()
            self.producer.channel.basic_publish(exchange=self.producer.exchange, routing_key=self.getRoutingKey(), body=message)
            # print('Sent ' + message)
            time.sleep(self.freq)

    def getMessage(self):
        return "Sensor.getMessage not overridden!"

    def getValue(self):
        eel.setText(self.id, self.value)
        #return "Sensor.getValue not overridden!"

    def getResponse(self):
        msg = {'function': self.function, 'id': self.id, 'location': self.location.toString(), 'type': self.typ, 'value': None}
        return msg

    def setEnvEffect(self, typ, effect):
        self.envEffect[typ] = effect

    def start(self):
        Thread(target=self.send, args=[]).start()
        Thread(target=self.consumer.start, args=[]).start()
