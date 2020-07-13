from threading import Thread
import eel
import time

from context_processor import ContextBridge
from mq.Consumer import Consumer
from mq.Producer import Producer
from gateway import Gateway
from realWorld.Environment import Environment

from realWorld.Location import Location
from realWorld.Climate import Climate
# sensor imports
from sensors.CO2Sensor import CO2Sensor
from sensors.ClockSensor import ClockSensor
from sensors.MotionSensor import MotionSensor
from sensors.TempSensor import TempSensor
from sensors.LightSensor import LightSensor
from sensors.PressureSensor import PressureSensor
from sensors.HumiditySensor import HumiditySensor
from sensors.PlugSocketSensor import PlugSocketSensor
from sensors.SoundLevelMeterSensor import SoundLevelMeterSensor
from sensors.WeatherForecastSensor import WeatherForecastSensor
# actuator imports
from actuators.LightActuator import LightActuator
from actuators.WindowActuator import WindowActuator
from actuators.SoundAwarenessActuator import SoundAwarenessActuator
from actuators.ClimateControllerActuator import ClimateControllerActuator

from settings import *

if __name__ == '__main__':

    # define eel functions and init webserver
    def GetObjectById(id):
        for i in range(0, len(objects)):
            if (objects[i].id == id):
                return objects[i]


    def GetObjectsByType(typ):
        results = []
        for i in range(0, len(objects)):
            if objects[i].typ == typ:
                results.append(objects[i].id)
        return results

    @eel.expose
    def eelLightOn(id):
        a =GetObjectById("device_la_"+ str(id))
        print("light on called for "+str(id))
        a.lightOn("js")

    @eel.expose
    def eelLightOff(id):
        a = GetObjectById("device_la_" + str(id))
        print("light off called for "+str(id))
        a.lightOff("js")

    @eel.expose
    def eelAddPerson():
        ms = GetObjectById("device_motion_1")
        ms.addPerson()


    @eel.expose
    def eelRemovePerson():
        ms = GetObjectById("device_motion_1")
        ms.removePerson()


    @eel.expose
    def eelGetSensors():
        tempsO = GetObjectsByType("temperatureOut")
        humO = GetObjectsByType("humidityOut")
        temps = GetObjectsByType("temperature")
        hum = GetObjectsByType("humidity")
        pressure = GetObjectsByType("pressure")
        motion = GetObjectsByType("motion")
        clock = GetObjectsByType("clock")
        co2 = GetObjectsByType("co2")
        light = GetObjectsByType("light_sensor")
        sls = GetObjectsByType("sound_level")
        windows = GetObjectsByType("window")
        acs = GetObjectsByType("climate_control")
        return clock + motion + tempsO + humO + temps + hum + co2 + pressure + light + sls + windows + acs


    @eel.expose
    def eelGetSensorValue(id):
        return [id, GetObjectById(id).getValue()]


    @eel.expose
    def eelSensorOverride(id, value):
        GetObjectById(id).overrideValue(value)


    @eel.expose
    def eelSensorOverrideStop(id):
        GetObjectById(id).overrideStop()


    def eelStart():
        time.sleep(3)
        eel.init('web')
        eel.start('main.html', host="localhost", cmdline_args=['--start-fullscreen'])

    # Start simulating climate
    climate = Climate("stuttgart", 20190709, 600)
    climate.sim()

    # Initialize rooms
    room1 = Location("U38", "0", "108")
    room2 = Location("U38", "0", "342")
    room3 = Location("U38", "0", "424")
    rooms = [room1, room2, room3]
    virtual_room = Location("none", "none", "none")

    objects = []

    """
         Creates and starts for our rooms the temperature, humidity, co2, and light sensors and the window and light 
         actuator (light bulb) 
         """
    for i in range(0, len(rooms)):
        # Sensors
        t = TempSensor(typ="temperature", id="device_temp_" + str(i), location=rooms[i], freq=update_frequency,
                       climate=climate, spread=3, stepSpread=0.5)
        t.start()
        objects.append(t)

        h = HumiditySensor(typ="humidity", id="device_hum_" + str(i), location=rooms[i], freq=update_frequency,
                           mean=45, spread=15, stepSpread=3)
        h.start()
        objects.append(h)

        c = CO2Sensor(typ="co2", id="device_co2_" + str(i), location=rooms[i], freq=update_frequency)
        c.start()
        objects.append(c)

        ls = LightSensor(typ="light_sensor", id="device_ls_" + str(i), location=rooms[i], freq=update_frequency, climate=climate, spread=8)
        ls.start()
        objects.append(ls)

        # Actuators
        w = WindowActuator(typ="window", id="device_w_" + str(i), location=rooms[i], freq=update_frequency,
                           consumer=Consumer("w_queue_" + str(i), "gateway.window_" + str(i)))
        w.start()
        objects.append(w)

        la = LightActuator(typ="light", id="device_la_" + str(i), location=rooms[i], freq=update_frequency,
                           consumer=Consumer("la_queue_" + str(i), "gateway.light_" + str(i)))
        la.start()
        objects.append(la)

        cc = ClimateControllerActuator(typ="climate_control", id="device_cc_" + str(i), location=rooms[i],
                                       freq=update_frequency,
                                       consumer=Consumer("cc_queue_" + str(i), "gateway.climate_" + str(i)))
        cc.start()
        objects.append(cc)

        #connect actuators to sensors
        Environment(cc, t).start()
        Environment(cc, h).start()
        Environment(cc, c).start()
        Environment(w, t).start()
        Environment(w, h).start()
        Environment(w, c).start()
        Environment(la, ls).start()

    """
     Creates and starts the clock and outside temperature sensor
    """
    cs = ClockSensor(typ="clock", id="clock", location=virtual_room, freq=1, climate=climate)
    cs.start()
    objects.append(cs)

    outSideTemp = TempSensor(typ="temperatureOut", id="Outside temperature", location=virtual_room, freq=1, climate=climate, spread=0, stepSpread=0)
    outSideTemp.start()
    objects.append(outSideTemp)

    outSideHum = HumiditySensor(typ="humidityOut", id="Outside humidity", location=virtual_room, freq=1,
                       mean=45, spread=15, stepSpread=3)
    outSideHum.start()
    objects.append(outSideHum)

    ls = LightSensor(typ="light_sensor", id="device_ls_outside", location=virtual_room, freq=update_frequency,
                     climate=climate, spread=8)
    ls.start()
    objects.append(ls)

    """
     Creates and starts the weather forecast api as a sensor
    """
    weather_forecast = WeatherForecastSensor(typ="weather_forecast", id="device_wfc_0", location=virtual_room,
                                             freq=update_frequency,
                                             city='Stuttgart', country='de', language='en')
    weather_forecast.start()
    objects.append(weather_forecast)

    """
     Creates for the number of tables (table_limit) the plug sockets and sound level meter sensors and the sound 
     awareness actuator (light) 
    """
    for i in range(table_limit[-1]):
        if i < table_limit[0]:
            loc = room1
        elif i < table_limit[1]:
            loc = room2
        else:
            loc = room3
        # Sensors
        p = PlugSocketSensor(typ="plug_socket", id="device_ps_" + str(i), location=loc, freq=update_frequency)
        p.start()
        objects.append(p)

        sls = SoundLevelMeterSensor(typ="sound_level", id="device_slms_" + str(i), location=loc, freq=update_frequency, spread=5, stepSpread=1)
        sls.start()
        objects.append(sls)

        # Actuators
        sla = SoundAwarenessActuator(typ="sound_level_actuator", id="device_slma_" + str(i), location=loc, freq=update_frequency,
                                     consumer=Consumer("saa_queue_" + str(i), "gateway.sound_level_" + str(i)))
        sla.start()
        objects.append(sla)

        Environment(sla, sls).start()

    """
     Creates and starts pressure sensors for our total number of seats (seat_limit)
    """
    for seatCounter in range(0, seat_limit[-1]):
        if seatCounter < seat_limit[0]:
            loc = room1
        elif seatCounter < seat_limit[1]:
            loc = room2
        else:
            loc = room3
        p = PressureSensor(typ="pressure", id="device_press_" + str(seatCounter), location=loc, freq=update_frequency)
        p.start()
        objects.append(p)

    # Connection between chairs and tables for presence recognition and sound generation
    for k, v in table_chair_map.items():
        table = GetObjectById(v)
        chair = GetObjectById(k)
        Environment(chair, table).start()


    """
     Creates and starts motion sensor at entrance
    """
    ms = MotionSensor(typ="motion", id="device_motion_1", location=room3, freq=5, rndValues=[0, 1, 2, 3],
                      probs=[0.7, 0.2, 0.05, 0.05], obj=objects)
    ms.start()
    objects.append(ms)

    gateway = Gateway(freq=update_frequency, producer=Producer(), consumer=Consumer("sensors", "*.*.*.*.*.*"))
    gateway.start()

    #con = ContextBridge(frequency=5, consumer=Consumer("context", "gateway.context"))
    #con.start()

    Thread(target=eelStart, args=[]).start()

