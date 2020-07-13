import json
import time
from threading import Thread

import eel

from actuators.Actuator import Actuator


class ClimateControllerActuator(Actuator):
    def __init__(self, typ, id, location, freq, consumer):
        super(ClimateControllerActuator, self).__init__(typ, id, location, freq, consumer)
        self.consumer.callback = self.receiveMessage
        self.status = False

    def getMessage(self):
        msg = self.getResponse()
        msg['value'] = self.status
        return json.dumps(msg)

    def receiveMessage(ch, method, properties, k, body):
        resp = body.decode('utf-8')
        if resp == 'True':
            ch.status = True
            ch.setEnvEffect('temperature', 1)
            ch.setEnvEffect('humidity', 6)
            ch.setEnvEffect('co2', -200)

            if (hasattr(eel, "setACStatus")):
                eel.setACStatus(ch.id, True)
            if (hasattr(eel, "setText")):
                eel.setText(ch.id, "on")

        else:
            ch.status = False
            ch.setEnvEffect('temperature', 0)
            ch.setEnvEffect('humidity', 0)
            ch.setEnvEffect('co2', 0)

            if (hasattr(eel, "setACStatus")):
                eel.setACStatus(ch.id, False)
            if (hasattr(eel, "setText")):
                eel.setText(ch.id, "off")

        #print("ClimateController_" + ch.location.room + ": " + body.decode('utf-8'))
