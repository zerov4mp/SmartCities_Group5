import json
import random
from sensors.Sensor import Sensor


class PlugSocketSensor(Sensor):
    occupied = False
    energy = 0
    counter = 0

    def getMessage(self):
        self.nextValue()
        msg = self.getResponse()
        msg['value'] = {'plug_socket_state': self.occupied, 'energy_consumption': self.energy}
        return json.dumps(msg)


    def nextValue(self):
        if self.occupied:
            self.counter = self.counter + 1
            if self.counter >= 3:
                self.counter = 0
                self.occupied = False
                self.energy = 0
            else:
                self.energy = random.randrange(10, 200, 10)
        else:
            self.occupied = random.choice([True,False])
            if self.occupied:
                self.energy = random.randrange(10, 200, 10)

