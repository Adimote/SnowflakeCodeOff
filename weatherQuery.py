__author__ = 'andy'
import requests

class weatherQuery:

    def __init__(self, api_key):
        self.key = api_key

    def getWeatherAt(self, lat, lon):
        # get the current weather in JSON
        self.request = requests.get('http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}'.format(lat,lon,self.key))
        if self.request.status_code != 200:
            print "Failed to get weather at location"
            return
        return self.how_bad_is_it(self.request.json())

    def how_bad_is_it(self, json):
        weather = json.get("weather")
        return weather[0].get("description")