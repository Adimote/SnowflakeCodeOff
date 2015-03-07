__author__ = 'andy'
import database
import weatherQuery

routesdatabase = database.dataBase()

weathermanager = weatherQuery.weatherQuery("5398a4c0be3fe2925cece3665658f661")

for flight, route in routesdatabase.data.items():
    print flight, ":"
    last_point = route[0]
    hour_count = 0
    for point in route:
        hour_count += routesdatabase.get_time_between(last_point, point)
        print point, "after ", hour_count, "hours, weather: ", weathermanager.getWeatherAt(point[0], point[1])
        last_point = point
