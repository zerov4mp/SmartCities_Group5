import json
import random
from realWorld.Location import Location
from mq.Producer import Producer
from sensors.Sensor import Sensor


class WindowSensor(Sensor):

    windowOpen = False
    state = "Closed"

    def getMessage(self):
        self.nextValue()
        msg = self.getResponse()
        msg['value'] = self.state
        return json.dumps(msg)


    def nextValue(self):
        self.windowOpen = random.choice([True,False])
        if self.windowOpen:
            self.state = "Opened"
        else:
            self.state = "Closed"
