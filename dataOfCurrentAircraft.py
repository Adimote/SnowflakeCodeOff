__author__ = 'andy'
import database
import weatherQuery

routesdatabase = database.dataBase()

weathermanager = weatherQuery.weatherQuery("5398a4c0be3fe2925cece3665658f661")

for flight in routesdatabase.getData():
    print flight["craft_id"]
    for point in flight["route"]:
        print weathermanager.getWeatherAt(point[0], point[1])
