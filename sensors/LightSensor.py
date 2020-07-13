import json
import random
import numpy as np

import eel

from sensors.Sensor import Sensor

class LightSensor(Sensor):


    def __init__(self, typ, id, location, freq, climate, spread):
        super(LightSensor, self).__init__(typ, id, location, freq)
        self.climate = climate
        self.value = 0
        self.optimum = 500
        self.spread = spread


    def getMessage(self):
        msg = self.getResponse()
        msg['value'] = self.getValue()
        return json.dumps(msg)

    def getValue(self):
        Sensor.getValue(self)

        hours = self.climate.clock // 60
        minutes = (self.climate.clock % 60)/60.0
        time = hours+minutes

        if(hasattr(eel,'dayLightScale')):
            scale = eel.dayLightScale(time)()
            if scale is None:
                scale = 1
        else:
            scale = 1

        # check if light actuator has effect
        if 'light_sensor' in self.envEffect:
            self.value = scale*self.optimum+self.envEffect['light_sensor']
        else:
            self.value = scale*self.optimum

        # spread for different values
        self.value = np.random.normal(self.value, self.spread)

        # clamp above zero
        if self.value < 0:
            self.value = 0

        return self.value




