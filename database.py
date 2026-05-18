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
                CREATE TABLE IF NOT EXISTS public.usuario(
                    nombre_del_usuario VARCHAR(50) PRIMARY KEY,
                    contrasena VARCHAR(50) NOT NULL,
                    rol VARCHAR(20) NOT NULL DEFAULT 'usuario' 
                    CHECK (rol IN ('admin', 'empleado', 'usuario')),
                    codigo_empleado INT REFERENCES public.empleado(codigo) ON DELETE SET NULL
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
                    ISBN VARCHAR(20),
                    titulo VARCHAR(150) NOT NULL,
                    autores VARCHAR(150) NOT NULL,
                    editorial VARCHAR(100) NOT NULL,
                    anio_publicacion INT NOT NULL CHECK (anio_publicacion > 0),
                    num_ejemplar INT NOT NULL CHECK (num_ejemplar >= 0),
                    PRIMARY KEY (ISBN, num_ejemplar)
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS public.prestamo(
                    codigo_prestamo SERIAL PRIMARY KEY,
                    isbn_libro VARCHAR(20) NOT NULL,
                    ejemplar_libro INT NOT NULL,
                    codigo_empleado INT NOT NULL REFERENCES public.empleado(codigo),
                    codigo_alumno VARCHAR(10) REFERENCES public.alumno(codigo),
                    codigo_profesor VARCHAR(10) REFERENCES public.profesor(codigo),
                    fecha_prestamo DATE NOT NULL,
                    fecha_entrega_limite DATE NOT NULL,
                    fecha_devolucion DATE,
                    estatus VARCHAR(20) NOT NULL DEFAULT 'Activo' CHECK (estatus IN ('Activo', 'Devuelto', 'Atrasado')),
                    multa DECIMAL(10,2) DEFAULT 0.00,
                    FOREIGN KEY (isbn_libro, ejemplar_libro) REFERENCES public.libro(ISBN, num_ejemplar),
                    CHECK (
                           (codigo_alumno IS NOT NULL AND codigo_profesor IS NULL) OR
                           (codigo_alumno IS NULL AND codigo_profesor IS NOT NULL))     
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
            query = "SELECT rol, codigo_empleado FROM public.usuario WHERE nombre_del_usuario = %s AND contrasena = %s;"
            cursor.execute(query, (usuario, contrasena)) 
            resultado = cursor.fetchone()

            if resultado:
                return resultado[0], resultado[1]
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

def registrar_profesor(codigo, nombre, direccion, telefono, sexo, fecha_nac, departamento,correo):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
            INSERT INTO public.profesor (codigo, nombre, direccion, telefono, sexo, fecha_nac, departamento, correo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (codigo,nombre,direccion,telefono,sexo,fecha_nac,departamento,correo))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al registrar: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

def registrar_libros(ISBN, titulo, autores, editorial, anio_publicacion, num_ejemplar):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
            INSERT INTO public.libro(ISBN, titulo, autores, editorial, anio_publicacion,num_ejemplar)
            VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (ISBN, titulo, autores, editorial, anio_publicacion, num_ejemplar))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al registrar: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

def registrar_prestamo(isbn_libro,ejemplar_libro, codigo_empleado,codigo_alumno,codigo_profesor,fecha_prestamo,fecha_entrega_limite,estatus,multa):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
            INSERT INTO public.prestamo(isbn_libro,ejemplar_libro, codigo_empleado,codigo_alumno,codigo_profesor,fecha_prestamo,fecha_entrega_limite,estatus,multa)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(query,(isbn_libro,ejemplar_libro, codigo_empleado,codigo_alumno,codigo_profesor,fecha_prestamo,fecha_entrega_limite,estatus,multa))
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

def obtener_profesores():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT codigo, nombre, direccion, telefono, sexo, fecha_nac, departamento, correo FROM public.profesor ORDER BY codigo;"
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

def obtener_libros():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT ISBN, titulo, autores, editorial, anio_publicacion, num_ejemplar from public.libro ORDER BY ISBN"
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

def obtener_libros_disponibles():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """SELECT ISBN, titulo, autores, editorial, anio_publicacion, num_ejemplar FROM public.libro 
                WHERE NOT EXISTS (SELECT 1 FROM public.prestamo WHERE public.prestamo.isbn_libro = public.libro.ISBN 
                      AND public.prestamo.ejemplar_libro = public.libro.num_ejemplar AND public.prestamo.estatus = 'Activo')
                ORDER BY ISBN;
            """
            cursor.execute(query)
            registros = cursor.fetchall()
            nombres_columnas = [desc[0].capitalize() for desc in cursor.description]
            return registros, nombres_columnas
        except Exception as e:
            print(f"Error al consultar disponibles: {e}")
            return None, None
        finally:
            cursor.close()
            conexion.close()
    return None, None

def obtener_prestamos():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT codigo_prestamo, isbn_libro, ejemplar_libro, codigo_empleado, codigo_alumno,codigo_profesor,fecha_prestamo,fecha_entrega_limite,fecha_devolucion,estatus,multa FROM public.prestamo ORDER BY codigo_prestamo;"
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

def obtener_prestamos_activos():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """SELECT p.codigo_prestamo, 
            COALESCE(a.nombre,pr.nombre) AS nombre_solicitante,l.titulo, p.ejemplar_libro, p.fecha_entrega_limite,
            CASE WHEN p.codigo_alumno IS NOT NULL THEN 'Alumno' ELSE 'Profesor' END AS tipo_solicitante,
            COALESCE(a.correo, pr.correo) AS correo
            FROM public.prestamo p
            LEFT JOIN public.alumno a ON p.codigo_alumno = a.codigo
            LEFT JOIN public.profesor pr ON p.codigo_profesor = pr.codigo
            JOIN public.libro l ON p.isbn_libro = l.ISBN AND p.ejemplar_libro = l.num_ejemplar
            WHERE p.estatus = 'Activo'
            ORDER BY p.codigo_prestamo;"""
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener préstamos activos: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()
    return None

def procesar_devolucion(codigo_prestamo,fecha_devolucion,multa):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """UPDATE public.prestamo SET fecha_devolucion = %s, estatus = 'Devuelto', multa = %s
                       WHERE codigo_prestamo = %s"""
            cursor.execute(query,(fecha_devolucion,multa,codigo_prestamo))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al procesar devolución: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False