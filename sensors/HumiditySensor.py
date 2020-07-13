# coding=utf-8
import json
import numpy as np
from random import random
from sensors.Sensor import Sensor

class HumiditySensor(Sensor):

    def __init__(self, typ, id, location, freq, mean, spread, stepSpread):
        super(HumiditySensor, self).__init__(typ, id, location, freq)
        self.value = 0
        self.mean = mean
        self.spread = spread
        self.stepSpread = stepSpread

    def getMessage(self):
        msg = self.getResponse()
        msg['value'] = self.getValue()
        return json.dumps(msg)

    def reset(self):
        self.value = np.random.normal(self.mean, self.spread)

    def getValue(self):
        Sensor.getValue(self)

        env = 0
        if 'humidity' in self.envEffect:
            env = self.envEffect['humidity']


        if(self.value ==0):
            #init sensor value
            self.reset()
        else:
            if(self.value < 10 or self.value >90):
                self.reset()
            if(self.value>50):
                env = -env
            if(env != 0):
                self.value = self.value + env
            else:
                self.value = np.random.normal(self.value, self.stepSpread)+env


        return self.value


