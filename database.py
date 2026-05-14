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

def inicializar_tablas():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS public.usuario(
                    nombre_del_usuario VARCHAR(50) PRIMARY KEY,
                    contrasena VARCHAR(50) NOT NULL,
                    rol VARCHAR(20) NOT NULL DEFAULT 'usuario' 
                    CHECK (rol IN ('admin', 'empleado', 'usuario'))
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS public.empleado(
                    codigo INT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    direccion VARCHAR(150) NOT NULL,
                    telefono VARCHAR(20) NOT NULL,
                    sexo CHAR(1) NOT NULL CHECK (sexo IN ('M', 'F')),
                    fecha_de_nac DATE NOT NULL,
                    turno VARCHAR(20) NOT NULL CHECK (turno IN ('Matutino', 'Vespertino'))
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS public.alumno(
                    codigo VARCHAR(10) PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    carrera VARCHAR(10) NOT NULL,
                    correo VARCHAR(100) NOT NULL UNIQUE,
                    direccion VARCHAR(150) NOT NULL,
                    telefono VARCHAR(20) NOT NULL,
                    sexo CHAR(1) NOT NULL CHECK (sexo IN ('M', 'F')),
                    fecha_nac DATE NOT NULL
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS public.profesor(
                    codigo VARCHAR(10) PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    direccion VARCHAR(150) NOT NULL,
                    telefono VARCHAR(20) NOT NULL,
                    sexo CHAR(1) NOT NULL CHECK (sexo IN ('M', 'F')),
                    fecha_nac DATE NOT NULL,
                    departamento VARCHAR(50) NOT NULL,
                    correo VARCHAR(100) NOT NULL UNIQUE
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS public.libro(
                    ISBN VARCHAR(20) PRIMARY KEY,
                    titulo VARCHAR(150) NOT NULL,
                    autores VARCHAR(150) NOT NULL,
                    editorial VARCHAR(100) NOT NULL,
                    anio_publicacion INT NOT NULL CHECK (anio_publicacion > 0),
                    num_ejemplar INT NOT NULL DEFAULT 1 CHECK (num_ejemplar >= 0)
                );
            ''')

            conexion.commit()
            print("Base de datos actualizada con éxito: Tablas, Constraints y Roles verificados.")
            
        except Exception as e:
            print(f"Error al inicializar base de datos: {e}")
            conexion.rollback()
        finally:
            cursor.close()
            conexion.close()

def validar_usuario(usuario, contrasena):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT rol FROM public.usuario WHERE nombre_del_usuario = %s AND contrasena = %s;"
            cursor.execute(query, (usuario, contrasena)) 
            resultado = cursor.fetchone()

            if resultado:
                return resultado[0]
            return None
        except Exception as e:
            print(f"Error en validación: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()
    return None    

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

def registrar_alumno(codigo,nombre,carrera,correo,direccion,telefono,sexo,fecha_nac):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
            INSERT INTO public.alumno (codigo, nombre, carrera, correo, direccion, telefono, sexo, fecha_nac)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (codigo,nombre,carrera,correo,direccion,telefono,sexo,fecha_nac))
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

def obtener_alumnos():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT codigo, nombre, carrera, correo, direccion, telefono, sexo, fecha_nac FROM public.alumno ORDER BY codigo;"
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