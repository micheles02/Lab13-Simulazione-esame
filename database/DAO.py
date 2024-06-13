from database.DB_connect import DBConnect
from model.States import State
from model.Sighting import Sighting
class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getAllStates():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from state s  """

        cursor.execute(query)

        for row in cursor:
            result.append(State(row["id"], row["Name"], row["Capital"], row["Lat"], row["Lng"], row["Area"], row["Population"], row["Neighbors"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllSighting():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from sighting s order by `datetime` asc """

        cursor.execute(query)

        for row in cursor:
            result.append(Sighting(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllShapes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct shape from sighting s 
                   where shape != "" """

        cursor.execute(query)

        for row in cursor:
            result.append(row['shape'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllWeightedNeigh(year,shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT n.state1, n.state2 , count(*) as N
                    FROM sighting s , neighbor n 
                    where year(s.`datetime`) = %s
                    and s.shape = %s
                    and (s.state = n.state1 or s.state = n.state2 )
                    and n.state1 < n.state2
                    group by n.state1 , n.state2 """

        cursor.execute(query, (year,shape))

        for row in cursor:
            result.append((row['state1'],row['state2'], row["N"]))

        cursor.close()
        conn.close()
        return result