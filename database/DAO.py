from database.DB_connect import DBConnect
from model.state import State


class DAO():
    def __init__(self):
        pass



    @staticmethod
    def getYear():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary = True)

        query = """select distinct YEAR(s.`datetime`) as year
                    from sighting s 
                    order by year"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getShape():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select distinct s.shape 
                    from sighting s 
                    order by shape 
                    """

        cursor.execute(query)

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select s.*
                   from state s"""

        cursor.execute(query)

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArchi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select distinctrow s1.id as s1, s2.id as s2
                    from state s1, state s2, neighbor n
                    where (s1.id = n.state1 and s2.id = n.state2) 
                    or (s2.id = n.state1 and s1.id = n.state2)
                   """

        cursor.execute(query)

        for row in cursor:
            result.append((row["s1"], row["s2"]))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getPeso(year, shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select n.state1, n.state2, count(*) as peso
                   from sighting s, neighbor n
                   where year(s.datetime) = %s
                   and s.shape = %s
                   and (s.state = n.state1 or s.state = n.state2)
                   group by n.state1, n.state2
                           """

        cursor.execute(query, (year, shape,))

        for row in cursor:
            result.append((row["state1"], row["state2"], row["peso"]))

        cursor.close()
        conn.close()
        return result

