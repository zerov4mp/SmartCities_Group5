# coding=utf-8
from random import random, uniform

import eel

from sensors.Sensor import Sensor
import json
import numpy as np



class TempSensor(Sensor):

    def __init__(self, typ, id, location, freq, climate, spread, stepSpread):
        super(TempSensor, self).__init__(typ, id, location, freq)
        self.climate = climate
        self.spread = spread
        self.stepSpread = stepSpread
        self.value = climate.temperature


    def getMessage(self):
        msg = self.getResponse()
        msg['value'] = self.getValue()
        return json.dumps(msg)

    def overrideValue(self, value):
        self.override = True
        self.value = value

    def getValue(self):
        Sensor.getValue(self)

        env = 0
        if 'temperature' in self.envEffect:
            env = self.envEffect['temperature']




        if(not self.override):
            if(self.value == 0):
                self.value = np.random.normal(self.climate.temperature, self.spread)+env
            else:
                if (self.value > 21):
                    env = -env

                if self.typ == "temperatureOut":
                    self.value = np.random.normal(self.climate.temperature, self.stepSpread)
                else:
                    if env != 0:
                        self.value = self.value+env

                        if (hasattr(eel, "setACMode")):

                            #get AC
                            for k in self.envEffect:
                                if 'cc' in k:
                                    if env > 0:
                                        eel.setACMode(k, True)
                                    else:
                                        eel.setACMode(k, False)

                    else:
                        self.value = np.random.normal(self.value, self.stepSpread) + env




        return self.value



