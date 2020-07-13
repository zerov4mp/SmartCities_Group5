import datetime

import pandas as pd
import numpy as np
import threading

class Climate():
    def __init__(self,station, startDate, dayDuration):
        self.station = station
        self.file = "realWorld/climate_"+station+".csv"

        data = pd.read_csv(self.file, sep=";", header=0)

        self.data = data
        self.temperature = 0

        self.time = 0
        self.index = 0
        self.clock = 0
        self.date = startDate
        self.dayDuration = dayDuration
        self.coeffs = [0, 0, 0]

    def nextDay(self):
        self.time = 0
        row = self.data.iloc[self.index, :]
        self.date = row["MESS_DATUM"]
        minT = row["TNK"]
        maxT = row["TXK"]
        return self.quadraticInterpolation(0, minT, 12*60, maxT, 24*60, minT)

    def sim(self):
        if self.time == 0:
            self.index = int(self.data[self.data["MESS_DATUM"] == self.date].index[0])
            self.coeffs = self.nextDay()

        if self.time > 24*60:
            self.index += 1
            self.coeffs = self.nextDay()

        self.clock = (self.time % (24.0*60))
        self.temperature = (self.coeffs[0]*(self.clock**2))+self.coeffs[1]*self.clock+self.coeffs[2]
        d = datetime.datetime.strptime(str(self.date), '%Y%m%d')
        # print("climate date: "+"{:%d.%m.%Y}".format(d)+" time is "+"{:.0f}".format(self.clock//60).zfill(2)+":"+"{:.0f}".format(self.clock%60).zfill(2)+". Current outside temperature "+"{:.2f}".format(self.temperature))
        self.time += (24.0*60) / self.dayDuration
        threading.Timer(1, self.sim).start()


    def quadraticInterpolation(self, x1, y1, x2, y2, x3, y3):
        denom = (x1 - x2) * (x1 - x3) * (x2 - x3)
        A = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom
        B = (x3 * x3 * (y1 - y2) + x2 * x2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / denom
        C = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / denom
        return A, B, C




