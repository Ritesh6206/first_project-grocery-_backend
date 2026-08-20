'''import mysql.connector
__cnx = None

def get_sql_connection():
    global __cnx
    if __cnx is None:
        import mysql.connector
        __cnx = mysql.connector.connect(user='root', password='------',
                                    host='localhost',
                                    database='grocery')
    return __cnx'''
'''cnx = mysql.connector.connect(user='root', password='------',
                                host='localhost',
                                database='grocery')'''



import mysql.connector

__cnx = None


def get_sql_connection():
    global __cnx

    if __cnx is None or not __cnx.is_connected():
        __cnx = mysql.connector.connect(
            user='root',
            password='-------',
            host='localhost',
            database='grocery'
        )

    return __cnx