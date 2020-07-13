import json

import eel

from actuators.Actuator import Actuator


class LightActuator(Actuator):
    def __init__(self, typ, id, location, freq, consumer):
        super(LightActuator, self).__init__(typ, id, location, freq, consumer)
        self.consumer.callback = self.receiveMessage
        self.status = False
        self.lux = 250

    def getMessage(self):
        msg = self.getResponse()
        msg['value'] = self.status
        return json.dumps(msg)

    def lightOn(self, caller="python"):
        self.setEnvEffect('light_sensor',self.lux)
        id = int(''.join(filter(str.isdigit, self.id)))
        if caller == "python" and hasattr(eel, 'lightOnJS'):
            method = getattr(eel, 'lightOnJS')
            method(id)()

    def lightOff(self, caller='python'):
        self.setEnvEffect('light_sensor',0)
        id = int(''.join(filter(str.isdigit, self.id)))
        if caller == "python" and hasattr(eel, 'lightOffJS'):
            method = getattr(eel, 'lightOffJS')
            method(id)()

    def receiveMessage(ch, method, properties, k, body):
        resp = body.decode('utf-8')
        if resp == 'True':
            ch.status = True
            ch.lightOn()
        else:
            ch.status = False
            ch.lightOff()
        #print("Light_" + ch.location.room + ": " + body.decode('utf-8'))
