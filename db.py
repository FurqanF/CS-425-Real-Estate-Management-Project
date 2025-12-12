import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="Real_Estate_Management_Database",
        user="postgres",
        password="admin"
    )