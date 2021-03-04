import psycopg2

def makeconnection(host, database, user, password):
    connection = psycopg2.connect(
                    host=host,
                    database=database,
                    user=user,
                    password=password)
    return connection


def makecursor(connection):
    return connection.cursor()


def closeconnection(connection, cursor):
    cursor.close()
    connection.close()