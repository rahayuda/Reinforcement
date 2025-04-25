import mysql.connector

def get_conn(db_name):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=db_name,
        port=3306
    )
