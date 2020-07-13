import json
from random import randrange, random

from mq.Producer import Producer
from realWorld.Location import Location
from sensors.Sensor import Sensor
import numpy as np


class SoundLevelMeterSensor(Sensor):

    def __init__(self, typ, id, location, freq, spread, stepSpread):
        super(SoundLevelMeterSensor, self).__init__(typ, id, location, freq)
        self.value = 0
        self.optimum = 35
        self.spread = spread
        self.stepSpread = stepSpread


    def getMessage(self):
        msg = self.getResponse()
        msg['value'] = self.getValue()
        return json.dumps(msg)

    def reset(self):
        env = 0
        if 'sound_level' in self.envEffect:
            env = self.envEffect['sound_level']
        self.value = np.random.normal(self.optimum, self.spread)+env

    def getValue(self):
        Sensor.getValue(self)

        env_sa = 0
        env_ps = 0
        
        if 'sound_level' in self.envEffect:
            env_sa = self.envEffect['sound_level']
        if 'sound_sensor' in self.envEffect:
            env_ps = self.envEffect['sound_sensor']

        if(not self.override):
            if(self.value == 0):
                self.reset()
            else:
                self.value = np.random.normal(self.value, self.stepSpread)+env_sa+env_ps

        # clamp above zero
        if self.value < 0:
            self.value = 0

        return self.value

