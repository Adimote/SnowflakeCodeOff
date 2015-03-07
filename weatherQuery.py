__author__ = 'andy'
import requests

class weatherQuery:

    def __init__(self, api_key):
        self.key = api_key

    def getWeatherAt(self, lat, lon):
        # get the current weather in JSON
        self.request = requests.get('http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}'.format(lat, lon, self.key))
        if self.request.status_code != 200:
            print "Failed to get weather at location"
            return (-1,"Couldn't get weather")

        try:
            weather = self.how_bad_is_it(self.request.json())
        except:
            weather = (-1, "Couldn't read weather")
        return weather

    def how_bad_is_it(self, json):
        windiness = json.get("wind")["speed"]
        if windiness < 6:
            desc = "Calm wind"
        elif windiness < 7:
            desc = "Very Mildly Windy"
        elif windiness < 9:
            desc = "Mildly Windy"
        elif windiness < 10:
            desc = "Slightly Windy"
        elif windiness < 15:
            desc = "Partly Windy"

        return (windiness,desc)