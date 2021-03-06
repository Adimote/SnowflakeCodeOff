__author__ = 'andy'
import database
import weatherQuery

WIND_WARNING_THRESHOLD = 6.5

routesdatabase = database.dataBase()

weathermanager = weatherQuery.weatherQuery("5398a4c0be3fe2925cece3665658f661")

for flight, route in routesdatabase.data.items():
    print "Flight", flight, ":"
    last_point = route[0]
    hour_count = 0
    printed = False
    for point in route:
        hour_count += routesdatabase.get_time_between(last_point, point)
        windiness = weathermanager.getWeatherAt(point[0], point[1])
        # if it's more than a bit windy
        if windiness[0] > WIND_WARNING_THRESHOLD:
            printed = True
            print "    ({:.4f},{:.4f}) after {:.2f} hours, Windiness: ({:.2f}mph) '{:}'".format(
                point[1], point[0], hour_count, windiness[0], windiness[1]
            )
        last_point = point
    if not printed:
        print "   All Good."
