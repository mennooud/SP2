import psycopg2

def makeconnection(host, database, user, password):
    '''Deze functie maakt een connectie met een PGAdmin database'''
    connection = psycopg2.connect(
                    host=host,
                    database=database,
                    user=user,
                    password=password)
    return connection


def makecursor(connection):
    '''Deze functie maakt een cursor die nodig is om queries uit te voeren'''
    return connection.cursor()


def closeconnection(connection, cursor):
    '''Deze functie sluit de connectie met de PGAdmin database'''
    cursor.close()
    connection.close()


def insertdata(cursor, query, values):
    '''Deze functie voert data in in de database'''
    cursor.execute(query, values)


def getdata(cursor, query, values, fetchone=True):
    '''Deze functie haalt data op uit de PGAdmin database'''
    cursor.execute(query, values)
    if fetchone:
        return cursor.fetchone()
    return cursor.fetchall()