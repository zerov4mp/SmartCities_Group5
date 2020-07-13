import json
import random

import eel

from realWorld.Location import Location
from mq.Producer import Producer
from sensors.Sensor import Sensor
import numpy as np


class MotionSensor(Sensor):

    def __init__(self, typ, id, location, freq, rndValues, probs, obj):
        super(MotionSensor, self).__init__(typ, id, location, freq)
        self.rndValues = np.array(rndValues, dtype=int)
        self.probs = np.array(probs, dtype=float)
        self.arriving = 0
        self.leaving = 0
        self.personCounter = 0
        self.obj = obj
        self.msg = ""

    def getMessage(self):
        oldPersonCount = self.personCounter
        self.getValue()

        msg = self.getResponse()
        msg['value'] = str(self.arriving)
        self.msg = json.dumps(msg)
        if(hasattr(eel,"setText")):
            data =  {'Person Counter': str(oldPersonCount), 'Arriving now':str(self.arriving), 'Leaving now':str(self.leaving)}
            msg=  {'sender': 'motion_sensor', 'data': data}
            eel.setText(self.id, json.dumps(msg))

        for i in range(0,(self.leaving)):
            self.personLeaves()

        self.leaving = 0
        self.arriving = 0
        return self.msg

    def addPerson(self):
        if self.leaving == 0:
            print("add person by frontend")
            self.arriving += 1
            self.personCounter += 1

    def removePerson(self):
        if(self.arriving == 0 and self.leaving <= self.personCounter):
            print("remove person by frontend")
            self.leaving += 1
            self.personCounter -= 1

    def personLeaves(self):

        rooms = dict()
        for o in self.obj:
            if o.typ == "pressure" and o.value == True:
               if o.location.room in rooms:
                   rooms[o.location.room].append(o)
               else:
                   #print("found room :"+o.location.room)
                   rooms[o.location.room] = [o]

        max = 0
        maxR = ""
        for r in rooms:
            count = len(rooms[r])
            if count > max:
                #print(r +" has count "+ str(count))
                max = count
                maxR = r

        if len(maxR)>0:
            #print("removing person from room "+maxR)
            chair = random.choice(rooms[maxR])
            chair.free()


    def getValue(self):

        if self.arriving == 0 and self.leaving == 0:
            if random.random() > 0.5:
                self.arriving = np.random.choice(a=self.rndValues, p=self.probs)+self.arriving
                self.personCounter += self.arriving
            else:
                l = np.random.choice(a=self.rndValues, p=self.probs)
                if (l+self.leaving) <= self.personCounter:
                    self.leaving = l+self.leaving
                    self.personCounter -= self.leaving


        #print("person counter: "+str(self.personCounter))
        #print("arriving: "+str(self.arriving))
        #print("leaving: "+str(self.leaving))





