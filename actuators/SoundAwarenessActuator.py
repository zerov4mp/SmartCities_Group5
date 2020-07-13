import json
import time
from threading import Thread

import eel

from actuators.Actuator import Actuator


class SoundAwarenessActuator(Actuator):
    def __init__(self, typ, id, location, freq, consumer):
        super(SoundAwarenessActuator, self).__init__(typ, id, location, freq, consumer)
        self.consumer.callback = self.receiveMessage
        self.status = False
        self.dB = -10

    def getMessage(self):
        msg = self.getResponse()
        msg['value'] = self.status
        return json.dumps(msg)

    def receiveMessage(ch, method, properties, k, body):
        resp = body.decode('utf-8')
        if resp == 'True':
            ch.status = True
            ch.setEnvEffect('sound_level', ch.dB)
            if (hasattr(eel, "setSoundActuatorStatus")):
                eel.setSoundActuatorStatus(ch.id, True)
            Thread(target=ch.resetStatus, args=[5]).start()
        else:
            ch.status = False


        idx = ch.id.split("_")[-1]
        #print("SoundAwarenssActuator_" + ch.location.room + "_Table[" + idx + "]" + ": " + body.decode('utf-8'))

    def resetStatus(self, seconds):
        time.sleep(seconds)
        self.status = False
        eel.setSoundActuatorStatus(self.id, False)
        self.setEnvEffect('sound_level', 0)


