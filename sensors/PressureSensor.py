import json
import random
from threading import Thread

import eel

from mq.Consumer import Consumer
from sensors.Sensor import Sensor


class PressureSensor(Sensor):

    def __init__(self, typ, id, location, freq):
        super(PressureSensor, self).__init__(typ, id, location, freq)
        idx = id.split("_")[-1]
        self.consumer = Consumer("pressure_queue_" + idx, "gateway.place_person_" + idx)
        self.consumer.callback = self.receiveMessage
        self.value = False
        Thread(target=self.consumer.start, args=[]).start()

    def receiveMessage(ch, method, properties, k, body):
        resp = json.loads(body.decode('utf-8'))
        ch.value = True
        print("Chair/PressureSensor_" + ch.location.room + ": " + body.decode('utf-8'))

    def getMessage(self):
        if(self.getValue()):
            msg = self.getResponse()
            msg["value"] = True
        else:
            msg = self.getResponse()
            msg['value'] = False
        return json.dumps(msg)

    def getValue(self):

        if(self.value):
            if(random.random()<0.33):
                self.envEffect['sound_sensor'] = 5
            else:
                self.envEffect['sound_sensor'] = 0
        else:
            self.envEffect['sound_sensor'] = 0

        if(hasattr(eel,"setText")):
            if(self.value):
                eel.setText(self.id, "occupied")
            else:
                eel.setText(self.id, "free")

        #if(not self.override and random.random() < 0.5):
         #   self.value = not self.value
        if hasattr(eel,'setChairStatus'):
            eel.setChairStatus(self.id, self.value)

        return self.value

    def free(self):
        self.value = False
        self.getValue()

    def overrideValue(self, value):
        self.override = True
        if(value=="True"):
            self.value = True
        else:
            self.value = False



