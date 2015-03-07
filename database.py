__author__ = 'andy'
import psycopg2


class dataBase:

    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname='routes' user='codeoff' host='sw29g08-snowflake.ecs.soton.ac.uk' password='codeoff'")
        except:
            print "Failed to connect"

        self.data = self.__query()

    def __query(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT "RSGUID_RTEUID_TXTDESIG",ST_AsText("ROUTESEGASLINE") FROM "RTE_SEG" WHERE "RTE_SEG"."ROUTESEGASLINE" && ST_MakeEnvelope(-2,50.0,-1,51.0,4326);""")
        return self.__parse_text_to_geom(cur.fetchall())

    def __parse_text_to_geom(self, data):
        newdata = []
        for row in data:
            newdata.append({
            "craft_id":row[0],
            # Do some scraggy parsing of the text into latlongs
            "route": self.__linestring_to_array(row[1])
            })
        return newdata

    def __linestring_to_array(self,linestring):
        data = linestring[11:-1]
        pointstrarray = data.split(",")
        # split ["1 50","4 2"] into [(1,50),(4,2)]
        point1 = tuple([float(i) for i in pointstrarray[0].split(" ")])
        point2 = tuple([float(i) for i in pointstrarray[1].split(" ")])
        return [point1, point2]

    def getData(self):
        # Returns a Dictionary of
            # Flight code
            # Array of points in route
        return self.data