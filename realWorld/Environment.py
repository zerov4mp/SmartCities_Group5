import datetime

import pandas as pd
import numpy as np
import threading
import time


class Environment():
    def __init__(self, actuator, sensor):
        self.actuator = actuator
        self.sensor = sensor

    def update(self):
        while (True):
            self.sensor.envEffect[self.actuator.id] = "active"
            for k in self.actuator.envEffect:
                self.sensor.envEffect[k] = self.actuator.envEffect[k]
            time.sleep(3)

    def start(self):
        threading.Thread(target=self.update, args=[]).start()
