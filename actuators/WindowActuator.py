import json
import time
from random import randrange
from threading import Thread

import eel

from actuators.Actuator import Actuator
from mq.Consumer import Consumer
from mq.Producer import Producer
from realWorld.Location import Location


class WindowActuator(Actuator):
    def __init__(self, typ, id, location, freq, consumer):
        super(WindowActuator, self).__init__(typ, id, location, freq, consumer)
        self.consumer.callback = self.receiveMessage
        self.status = False
        Thread(target=self.initFrontend, args=[]).start()

    def getMessage(self):
        msg = self.getResponse()
        msg['value'] = self.status
        return json.dumps(msg)

    def initFrontend(self):
        time.sleep(10)
        if (hasattr(eel, "setWindowStatus")):
            eel.setWindowStatus(self.id, self.status)
        if (hasattr(eel, "setText")):
            eel.setText(self.id, "closed")

    def receiveMessage(ch, method, properties, k, body):
        resp = body.decode('utf-8')
        if resp == 'True':
            ch.status = True
            ch.setEnvEffect('temperature', 1)
            ch.setEnvEffect('humidity', 6)
            ch.setEnvEffect('co2', -200)

            if (hasattr(eel, "setWindowStatus")):
                eel.setWindowStatus(ch.id, True)
            if (hasattr(eel, "setText")):
                eel.setText(ch.id, "open")

        else:
            ch.status = False
            ch.setEnvEffect('temperature', 0)
            ch.setEnvEffect('humidity', 0)
            ch.setEnvEffect('co2', 0)
            if (hasattr(eel, "setWindowStatus")):
                eel.setWindowStatus(ch.id, False)
            if (hasattr(eel, "setText")):
                eel.setText(ch.id, "closed")

        #print("Window_" + ch.location.room + ": " + body.decode('utf-8'))
