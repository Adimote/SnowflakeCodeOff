__author__ = 'andy'
import requests

class weatherQuery:

    def __init__(self,api_key):
        self.key = api_key

    def getWeatherAt(self,lat,long):
        # get the current weather in JSON
        self.request = requests.get('http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}'.format(lat,long,self.key))
        if self.request.status_code != 200:
            print "Failed to get weather at location"
            return
        return self.__parse_json(self.request.json())

    def __parse_json(self, json):
        weather = json.get("weather")
        return weather[0].get("description")