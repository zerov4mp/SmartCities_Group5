# coding=utf-8
import datetime
from random import random, uniform

import eel

from sensors.Sensor import Sensor
import json


class ClockSensor(Sensor):

    def __init__(self, typ, id, location, freq, climate):
        super(ClockSensor, self).__init__(typ, id, location, freq)
        self.climate = climate
        self.value = climate.clock
        self.date = climate.date

    def getMessage(self):
        msg = self.getResponse()
        msg['value'] = self.getValue()
        return json.dumps(msg)

    def getValue(self):
        self.value = self.climate.clock
        self.date = self.climate.date

        d = datetime.datetime.strptime(str(self.date), '%Y%m%d')
        msg  = "{:%d.%m.%Y}".format(d)+"   "+"{:.0f}".format(self.value // 60).zfill(2) + ":" + "{:.0f}".format(int(self.value) % 60).zfill(2)

        if hasattr(eel, "setText"):
            eel.setText(self.id, msg)
        if hasattr(eel, "updateClock"):
            eel.updateClock(msg)
        return self.value
