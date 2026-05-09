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

def registrar_empleado(codigo, nombre, direccion, telefono, sexo, fecha_nac, turno):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
            INSERT INTO public.empleado (codigo, nombre, direccion, telefono, sexo, fecha_de_nac, turno)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (codigo, nombre, direccion, telefono, sexo, fecha_nac, turno))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al registrar: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

def obtener_empleados():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT codigo, nombre, direccion, telefono, sexo, fecha_de_nac, turno FROM public.empleado ORDER BY codigo;"
            cursor.execute(query)
            
            registros = cursor.fetchall()
            
            nombres_columnas = [desc[0].capitalize() for desc in cursor.description]
            
            return registros, nombres_columnas
        except Exception as e:
            print(f"Error al consultar: {e}")
            return None, None
        finally:
            cursor.close()
            conexion.close()
    return None, None