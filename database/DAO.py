from database.DB_connect import DBConnect
from model.prodotto import Prodotto


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getAllColor():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = """select distinct(Product_color)
                from go_products
                order by Product_color"""

        cursor.execute(query)

        for row in cursor:
            result.append(row[0])

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getAllProduct(color):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                        from go_products
                        where Product_color=%s"""

        cursor.execute(query,(color,))

        for row in cursor:
            result.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(p1Code,p2Code,year,idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = """select g1.Product_number,g2.Product_number, count(distinct(g1.`Date`)) as n
                from go_daily_sales g1 , go_daily_sales g2
                where g1.Product_number=%s 
                and g2.Product_number=%s 
                and g1.Retailer_code=g2.Retailer_code
                and g1.`Date`=g2.`Date`
                and year(g1.`Date`)=%s 
                group by g1.Product_number,g2.Product_number"""

        cursor.execute(query,(p1Code,p2Code,year))

        for row in cursor:
            result.append((idMap[row[0]],idMap[row[1]],row[2]))

        cursor.close()
        conn.close()
        return result
