import psycopg2

def makeconnection(host, database, user, password):
    connection = psycopg2.connect(
                    database='huwebshop',
                    user='postgres',
                    password='1234')
    return connection


def makecursor(connection):
    return connection.cursor()


def closeconnection(connection, cursor):
    cursor.close()
    connection.close()


def insertdata(cursor, query):
    cursor.execute(query)