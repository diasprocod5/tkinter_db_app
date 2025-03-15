import psycopg2
from psycopg2 import OperationalError


def connect_to_db(user, password, dbname="MyDB_CW"):
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host='localhost',
            port='5432'
        )
        print('Connected')
        return connection
    except OperationalError as e:
        print(f'Connection error: {e}')
        return None

def close_db_connection(connection):
    if connection:
        connection.close()
        print("Connection is closed")
    else:
        print("Not connected to db")
