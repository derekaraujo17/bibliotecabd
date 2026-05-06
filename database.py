import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

def conectar_bd():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            user="postgres",
            password=DATABASE_PASSWORD,
            database = "Biblioteca",
            port= "5432"
        )
        print("Conexion exitosa")
        return conexion
    except Error as e:
        print(f"Conexion fallada: {e}")

if __name__ == "__main__":
    conn = conectar_bd()
    if conn:
        conn.close()
        print("Conexion cerrada.")