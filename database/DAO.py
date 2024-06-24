from database.DB_connect import DBConnect



class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getLocalizzazioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.Localization as loc
                    from classification c 
                    order by c.Localization """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["loc"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select  distinctrow  c.Localization as l1, c2.Localization as l2, count(distinct i.`Type`) as conteggio
                from classification c , interactions i , classification c2 
                where c.Localization < c2.Localization 
                and ( (c2.GeneID = i.GeneID1 and c.GeneID = i.GeneID2) or (c.GeneID = i.GeneID1 and c2.GeneID = i.GeneID2) )
                group by c.Localization, c2.Localization  
                order by c.Localization, c2.Localization  """

        cursor.execute(query, ())

        for row in cursor:
            result.append([row["l1"], row["l2"], row["conteggio"]])

        cursor.close()
        conn.close()
        return result

