__author__ = 'andy'
import psycopg2
import math

class dataBase:

    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname='routes' user='codeoff' host='sw29g08-snowflake.ecs.soton.ac.uk' password='codeoff'")
        except:
            print "Failed to connect"

        self.data = self.__query()

    def __query(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT "RSGUID_RTEUID_TXTDESIG",ST_AsText("ROUTESEGASLINE") FROM "RTE_SEG" ;""") #WHERE "RTE_SEG"."ROUTESEGASLINE" && ST_MakeEnvelope(-2,50.0,-1,51.0,4326)
        return self.__parse_text_to_geom(cur.fetchall())

    def __parse_text_to_geom(self, data):
        new_data = {}
        for row in data:
            craft_id = row[0]
            # Do some scraggy parsing of the text into lat,lon
            line_segment = self.__linestring_to_tuple(row[1])
            if craft_id in new_data:
                new_data[craft_id].append(line_segment)
            else:
                new_data[craft_id] = [line_segment]

        # Sort the lines into the correct route
        ordered_lines = {}
        for key, row in new_data.items():
            ordered_lines[key] = self.__merge_route(row)

        # Get the points in the data
        ordered_routes = {}
        # Unique the points
        for flight, lines in ordered_lines.items():
            points = []
            for line in lines:
                if line[0] not in points:
                    points.append(line[0])
                if line[1] not in points:
                    points.append(line[1])
            ordered_routes[flight] = points
        return ordered_routes

    def __merge_route(self, current_route):
        linked_items = []
        # Construct a list of before, current, and after
        for line in current_route:
            linked_item = [None, line, None]
            for other_line in current_route:
                # if this line goes after the seen line
                if self.__close_enough(line[0], other_line[1]):
                    linked_item[0] = other_line
                # if this line goes before the seen line
                if self.__close_enough(line[1], other_line[0]):
                    linked_item[2] = other_line
            linked_items.append(linked_item)
        # find all elements without a beginning
        starts = [x for x in linked_items if not x[0]]
        # Make a list of all lists of tuples of points
        lists = [self.__build_list_from_linked_list(start, linked_items) for start in starts]
        # Return the first list
        return lists[0]

    def __build_list_from_linked_list(self, start, items):
        list = []
        cur = start
        list.append(cur[1])
        # Traverse the list
        while cur[2]:
            found = False
            for linked_item in items:
                if cur[2] == linked_item[1]:
                    cur = linked_item
                    found = True
                    break
            if not found:
                return list
            list.append(cur[1])
        return list

    def __close_enough(self, point1, point2):
        return point1 == point2

    def __linestring_to_tuple(self,linestring):
        data = linestring[11:-1]
        pointstrarray = data.split(",")
        # split ["1 50","4 2"] into ((1,50),(4,2))
        point1 = tuple([float(i) for i in pointstrarray[0].split(" ")])
        point2 = tuple([float(i) for i in pointstrarray[1].split(" ")])
        return (point1, point2)

    def get_time_between(self, latlon_a, latlon_b):
        """
        :return: Time between points in hours
        """
        lat1 = latlon_a[0]
        lat2 = latlon_b[0]
        lon1 = latlon_a[1]
        lon2 = latlon_b[1]
        diff_lat = math.radians(lat2-lat1)
        diff_lon = math.radians(lon2-lon1)

        ## Calculate the distance between a and b.
        a = math.sin(diff_lat/2) * math.sin(diff_lat/2) +\
        math.cos(lat1) * math.cos(lat2) *\
        math.sin(diff_lon/2) * math.sin(diff_lon/2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        # an aircraft goes at 550mph, aka 885000 metres per hour

        return (6371000*c)/885000


