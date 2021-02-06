import os
import sys
import utils.key_gen as keygen

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils.opendata as opendata


class Weather:

    def __init__(self, temp, feels_like, wind_speed, humidity, precipitation, weather_code):
        self.temp = temp
        self.feels_like = feels_like
        self.wind_speed = wind_speed
        self.humidity = humidity
        self.precipitation = precipitation
        self.weather_code = weather_code

    def encode(self):
        return self.__dict__

    @staticmethod
    def get_weather():
        # id must be a number, not a string
        weather = opendata.parse_json_data_weather()
        return Weather(temp=weather.get('temp'), feels_like=weather.get('feels_like'),
                       wind_speed=weather.get('wind_speed'), humidity=weather.get('humidity'),
                       precipitation=weather.get('precipitation'), weather_code=weather.get('weather_code'))
