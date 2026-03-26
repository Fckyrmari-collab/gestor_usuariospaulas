import mysql.connector

def conectar():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='empresa2026'
    )

    if conn.is_connected():
        print('Conexión exitosa a la base de datos')

    return conn

#conectar()

    