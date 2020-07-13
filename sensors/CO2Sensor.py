from random import randrange
import json
from sensors.Sensor import Sensor


class CO2Sensor(Sensor):
    def getMessage(self):
        msg = self.getResponse()
        msg['value'] = self.getValue()
        return json.dumps(msg)

    def partsPerMillionToPercent(self, ppm):
        return (ppm / 1000000)

    def ppmDangerLevel(self, ppm):
        if ppm <= 450:
            return 'Typical atmospheric concentration'
        elif ppm <= 800:
            return 'Acceptable indoor air quality'
        elif ppm <= 1000:
            return 'Tolerable indoor air quality'
        elif ppm <= 5000:
            return 'Average exposure limit over 8-hour period'
        elif ppm <= 35000:
            return 'Concern, short exposure only'
        elif self.partsPerMillionToPercent(ppm) <= 8:
            return 'Increased respiration rate, headach'
        elif self.partsPerMillionToPercent(ppm) < 20:
            return 'Nausea, vomiting, unconsciousness'
        else:
            return 'Rapid unconsciousness, death'

    def getValue(self):
        Sensor.getValue(self)

        choice = randrange(0, 1000, 1)
        if choice <= 900:
            ppm = randrange(0, 800, 1)
        elif choice <= 995:
            ppm = randrange(0, 1000, 1)
        elif choice <= 997:
            ppm = randrange(0, 5000, 1)
        elif choice == 998:
            ppm = randrange(0, 35000, 1)
        elif choice == 999:
            ppm = randrange(0, 8000000, 1)
        else:
            ppm = randrange(0, 21000000, 1)

        if 'co2' in self.envEffect:
            ppm = ppm+self.envEffect['co2']
            if ppm < 300:
                ppm = 300
        else:
            ppm = ppm

        if ppm < 0:
            self.value = 0
        else:
            self.value = ppm

        return self.value