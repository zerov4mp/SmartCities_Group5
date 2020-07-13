import json
import collections
import time
from threading import Thread
from mq.Consumer import Consumer

import eel

from ai_planner import update_problem_file_objects, update_problem_file_init, get_plan, sdd, sdp, sed, sep, \
    update_problem_file_goal, start_planning
from plan_executor import Executioner
from problem_writer import problem_writer


class ContextBridge:
    
    personCount = 0

    def __init__(self, frequency, consumer):
        self.consumer = consumer
        self.consumer.callback = self.receiveMessage
        self.system_state = self.create_recursive_dict()
        self.context_state = self.create_recursive_dict()
        self.context_state_outside = self.create_recursive_dict()
        self.freq = frequency
        self.executioner = Executioner()

    def create_recursive_dict(self):
        return collections.defaultdict(self.create_recursive_dict)

    def receiveMessage(self, method, properties, k, body):
        resp = json.loads(body.decode('utf-8'))
        self.system_state[resp['location']][resp['function']][resp['type']][resp['id']] = resp['value']
        if not resp['location'] == "none.none.none":
            self.context_state[resp['location']][resp['function']][resp['type']][resp['id']] = self.create_context(resp['type'], resp['value'])
        else:
            self.context_state_outside[resp['location']][resp['function']][resp['type']][resp['id']] = self.create_context(resp['type'], resp['value'])

    def create_context(self, type, value):
        if type == "temperature":
            if int(value) < 20:
                return "low"
            elif int(value) <22:
                return "mid"
            elif int(value) >=22:
                return "high"
        elif type == "humidity":
            if int(value) < 40:
                return "low"
            elif int(value) <60:
                return "mid"
            elif int(value) >=60:
                return "high"
        elif type == "co2":
            if int(value) < 1000:
                return "low"
            elif int(value) >=1000:
                return "high"
        elif type == "light_sensor":
            if int(value) < 200:
                return "low"
            elif int(value) >=200:
                return "high"
        elif type == "sound_level":
            if int(value) < 50:
                return "low"
            elif int(value) >=50:
                return "high"
        elif type == "window":
            return value
        elif type == "pressure":
            return value
        elif type == "climate_control":
            return value
        elif type == "light":
            return value
        elif type == "motion":
            self.personCount += int(value)
            return value
        elif type == "weatherforecast":
            if "rain" or "thunderstorm" or "drizzle" or "snow" in value:
                return True
            else:
                return False
        elif type == "temperatureOut":
            if int(value) < 20:
                return "low"
            elif int(value) <22:
                return "mid"
            elif int(value) >=22:
                return "high"
        elif type == "humidityOut":
            if int(value) < 40:
                return "low"
            elif int(value) <60:
                return "mid"
            elif int(value) >=60:
                return "high"



    def getSensorValue(self, type, room, context_state_copy):
        vals = list(context_state_copy[room]['sensor'][type].values())
        if(len(vals)>0):
            return vals[0]
        else:
            return None

    def getActuatorValue(self, type, room, context_state_copy):
        vals = list(context_state_copy[room]['actuator'][type].values())
        if(len(vals)>0):
            return vals[0]
        else:
            return None


    def update_problem(self):
        pw = problem_writer()

        #context_state_copy = copy.deepcopy(self.context_state)
        #context_state_outside_copy = copy.deepcopy(self.context_state_outside)
        context_state_copy = self.context_state
        context_state_outside_copy = self.context_state_outside

        # set objects
        pw.setRooms(len(context_state_copy))
        chairCounter = 1
        nOfChairs = 0
        nOfPersPerRoom = [0,0,0]
        tables = []
        for i, room in enumerate(context_state_copy):
            i += 1
            presence = False
            nOfChairs += len(context_state_copy[room]['sensor']['pressure'])
            for c in context_state_copy[room]['sensor']['pressure']:
                if context_state_copy[room]['sensor']['pressure'][c]:
                    nOfPersPerRoom[i-1] +=1
                    presence = True
                else:
                    pw.setFreeChair(chairCounter,i)
                chairCounter+=1
            if presence:
                pw.setPresence(i)


            roomTemp = list(context_state_copy[room]['sensor']['temperature'].values())[0]
            outsideTemp = list(context_state_outside_copy["none.none.none"]['sensor']['temperatureOut'].values())[0]

            if roomTemp == "low":
                if outsideTemp == ("mid" or "high"):
                    pw.setOutsideTemp("higher",i)
            if roomTemp == "high":
                if outsideTemp == ("mid" or "low"):
                    pw.setOutsideTemp("lower",i)
            if roomTemp == "mid":
                if outsideTemp == "low":
                    pw.setOutsideTemp("lower",i)
                elif outsideTemp == "high":
                    pw.setOutsideTemp("higher",i)

            roomHumidity =  list(context_state_copy[room]['sensor']['humidity'].values())[0]
            outsideHumidity = list(context_state_outside_copy["none.none.none"]['sensor']['humidityOut'].values())[0]

            if roomHumidity == "low":
                if outsideHumidity == ("mid" or "high"):
                    pw.setOutsideHum("higher",i)
            if roomHumidity == "high":
                if outsideHumidity == ("mid" or "low"):
                    pw.setOutsideHum("lower",i)
            if roomHumidity == "mid":
                if outsideHumidity == "low":
                    pw.setOutsideHum("lower",i)
                elif outsideHumidity == "high":
                    pw.setOutsideHum("higher",i)


            pw.setTemp(self.getSensorValue('temperature', room, context_state_copy), i)
            pw.setHum(self.getSensorValue('humidity', room, context_state_copy), i)

            if self.getSensorValue('co2', room, context_state_copy) == 'high':
                pw.setHighCO2(i)

            if self.getSensorValue('light_sensor', room, context_state_copy) == 'low':
                pw.setLowLight(i)

            for k,v in context_state_copy[room]['sensor']['sound_level'].items():
                tables.append(context_state_copy[room]['sensor']['sound_level'][k])


            # Actuators
            if self.getActuatorValue('window', room, context_state_copy):
                pw.setWindowOpen(i)

            if self.getActuatorValue('climate_control', room, context_state_copy):
                pw.setClimateOn(i)
            if self.getActuatorValue('light', room, context_state_copy):
                pw.setLightOn(i)


        pw.setTables(len(tables))
        for i,v in enumerate(tables):
            if v == "high":
                pw.setLoudSound(i+1)


        lowestNumOfPers = 0;
        if nOfPersPerRoom[0] < nOfPersPerRoom[1]:
            if nOfPersPerRoom[0] < nOfPersPerRoom[2]:
                lowestNumOfPers = nOfPersPerRoom[0]
            else:
                lowestNumOfPers = nOfPersPerRoom[2]
        elif nOfPersPerRoom[1] < nOfPersPerRoom[2]:
            lowestNumOfPers = nOfPersPerRoom[1]
        else:
            lowestNumOfPers = nOfPersPerRoom[2]

        nOfPersPerRoom[0] -= lowestNumOfPers
        nOfPersPerRoom[1] -= lowestNumOfPers
        nOfPersPerRoom[2] -= lowestNumOfPers

        i=0
        while i < len(nOfPersPerRoom):
            if nOfPersPerRoom[i] == 1:
                pw.setOnePersonMoreInRoom(i+1)
            elif nOfPersPerRoom[i] == 2:
                pw.setTwoPersonMoreInRoom(i+1)
            elif nOfPersPerRoom[i] == 3:
                pw.setThreePersonMoreInRoom(i+1)
            i +=1


        self.actPersonCount = self.personCount
        for k in range(1, self.actPersonCount + 1):
            pw.setNewPerson(k)

        if self.actPersonCount != 0:
            pw.setPersons(self.actPersonCount)

        for w, v in context_state_outside_copy["none.none.none"]['sensor']['weatherforcast'].items():
            if v:
                pw.setBadWeather()

        for l, v in context_state_outside_copy["none.none.none"]['sensor']['light_sensor'].items():
            if v == "low":
                pw.setLowLightOutside()
        pw.setChairs(nOfChairs)
        pw.finishObjects()
        pw.finishInit()
        pw.finishGoal()

        if (hasattr(eel, "setText")):
            data = {'context_distribution_problem': pw.initDistribution, 'context_environment_problem': pw.initEnvironment}
            msg = {'sender': 'ContextBridge', 'data': data}
            eel.setText("plan", json.dumps(msg))


        return pw, [pw.initEnvironment, pw.objectsEnvironment, pw.initDistribution, pw.objectsDistribution, pw.goalDistribution]

    def create_plan(self):
        time.sleep(6)
        while True:
            pw, _ = self.update_problem()
            update_problem_file_objects(sep, pw.objectsEnvironment)
            update_problem_file_init(sep, pw.initEnvironment)
            plan_name, plan = start_planning(sed, sep)
            self.executioner.execute_plan(plan_name)

            if self.actPersonCount != 0:
                update_problem_file_objects(sdp, pw.objectsDistribution)
                update_problem_file_init(sdp, pw.initDistribution)
                update_problem_file_goal(sdp, pw.goalDistribution)
                plan_name, plan = start_planning(sdd, sdp)

                self.executioner.execute_plan(plan_name)
                self.personCount -= self.actPersonCount
            time.sleep(self.freq)

    def start(self):
        Thread(target=self.consumer.start, args=[]).start()
        Thread(target=self.create_plan, args=[]).start()


if __name__ == '__main__':
    con = ContextBridge(frequency=5, consumer=Consumer("context", "gateway.context"))
    con.start()
