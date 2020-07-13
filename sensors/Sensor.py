from threading import Thread
import time


import eel

from mq.Producer import Producer


class Sensor:
    def __init__(self, typ, id, location, freq):
        self.typ = typ
        self.id = id
        self.location = location
        self.freq = freq
        self.producer = Producer()
        self.value = 0
        self.override = False
        self.envEffect = dict()

        self.function = 'sensor'

    def getRoutingKey(self):
        return self.location.building+"."+self.location.floor+"."+self.location.room+".sensor."+self.typ+"."+self.id

    def send(self):
        self.producer.channel.exchange_declare(exchange=self.producer.exchange, exchange_type="topic", durable=True, auto_delete=False)
        while True:
            message = self.getMessage()
            self.producer.channel.basic_publish(exchange=self.producer.exchange, routing_key=self.getRoutingKey(), body=message)
            # print('Sent ' + message)
            time.sleep(self.freq)

    def getMessage(self):
        return "Sensor.getMessage not overridden!"

    def overrideValue(self,value):
        return "Sensor.override is not implemented!"

    def overrideStop(self):
        self.override = False

    def getValue(self):
        if(hasattr(eel,"setText")):
            eel.setText(self.id, str(round(self.value,1)))
        #return "Sensor.getValue not overridden!"


    def getResponse(self):
        msg = {'function': self.function, 'id': self.id, 'location': self.location.toString() ,'type': self.typ, 'value': None}
        return msg


    def start(self):
        Thread(target=self.send, args=[]).start()

