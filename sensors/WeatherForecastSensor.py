from sensors.Sensor import Sensor
import requests
import json

from mq.Producer import Producer
from realWorld.Location import Location

api_key = '9c69b31391af4ccdf5727449bc03d324'


class WeatherForecastSensor(Sensor):
    def __init__(self, typ, id, location, freq, city, country, language):
        super(WeatherForecastSensor, self).__init__(typ, id, location, freq)
        self.city = city
        self.country = country
        self.lang = language

    def getMessage(self):
        msg = self.getResponse()
        msg['value'] = self.getForecast()
        return json.dumps(msg)

    def getWeatherData(self):
        api_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + self.city + ',' + self.country + '&appid=' + api_key + '&lang=' + self.lang
        response = requests.get(api_url)
        # print(response.text)
        weather = json.loads(response.text)
        return weather

    def getTemperature(self):
        weather = self.getWeatherData()
        # print(self.fahrenheitToCelsius(weather['main']['temp']))
        return self.kelvinToCelsius(weather['main']['temp'])

    def getForecast(self):
        weather = self.getWeatherData()
        # print(weather['weather'][0]['description'])
        return weather['weather'][0]['description']

    @staticmethod
    def kelvinToCelsius(kelvin):
        return kelvin - 273.5


if __name__ == '__main__':
    wfs_obj = WeatherForecastSensor("weather_forecast", "device_wfc_0", Location("V47", "0", "01"), 3, Producer(), 'Stuttgart', 'de', 'en')
    print(wfs_obj.getMessage())
