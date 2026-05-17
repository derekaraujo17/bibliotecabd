import streamlit as st
from helpers import render_header
from database import registrar_prestamo,obtener_libros,obtener_alumnos,obtener_profesores,obtener_empleados
import pandas as pd
import datetime

def mostrar_menu_prestamos():
    render_header()
    col1,col2 = st.columns([3,1])
    with col2:
        if st.button("⬅ Volver al Panel Principal"):
            st.session_state["pantalla_actual"] = "principal"
            st.rerun()
    st.markdown("<h2 style='text-align:center;'>Menú PRÉSTAMOS</h2>",unsafe_allow_html=True)
    st.divider()
    opcion = st.selectbox("Selecciona una opción:",
                          ["---","Registrar préstamo","Devolver préstamo","Consulta de préstamo","Consultas de préstamos"])
    if opcion == "Registrar préstamo":
        st.subheader("Registro de préstamos")
        libros_bd, columnas = obtener_libros()
        if not libros_bd:
            st.warning("No hay libros registrados en el catálogo aún.")
            return
        diccionario_libros = {
            f"{libro[0]}|{libro[5]}": f"{libro[1]} - Ejemplar: {libro[5]} (ISBN: {libro[0]})" 
            for libro in libros_bd
        }
        alumnos_bd,columnas = obtener_alumnos()
        diccionario_alumnos = {
            f"{alumno[0]}|{alumno[1]}": f"{alumno[0]} - {alumno[1]}"
            for alumno in alumnos_bd
        }
        profesores_bd,columnas = obtener_profesores()
        diccionario_profesores = {
            f"{profesor[0]}|{profesor[1]}": f"{profesor[0]} - {profesor[1]}"
            for profesor in profesores_bd
        }
        codigo_empleado_real = st.session_state.get("codigo_empleado")
        nombre_usuario_actual = st.session_state.get("usuario","")
        tipo_solicitante = st.radio("¿Quién solicita el préstamo?", ["Alumno","Profesor"],horizontal=True)

        with st.form("registro_prestamos",clear_on_submit=True):
            col_a,col_b = st.columns(2)
            with col_a:
                if tipo_solicitante == "Alumno":
                    codigo_solicitante = st.selectbox(
                        "Selecciona el código del alumno:",
                        options=list(diccionario_alumnos.keys()),
                        format_func=lambda x: diccionario_alumnos[x]
                    )
                else:
                    codigo_solicitante = st.selectbox(
                        "Selecciona el código del profesor:",
                        options=list(diccionario_profesores.keys()),
                        format_func=lambda x: diccionario_profesores[x]
                    )
                st.text_input("Código del Empleado que registra",value=str(codigo_empleado_real),disabled=True)
            with col_b:
                fecha_prestamo = st.date_input("Fecha del préstamo",
                                               min_value=datetime.date(2020,1,1),
                                               max_value=datetime.date.today(),
                                               format="DD/MM/YYYY")    
            isbn_seleccionados = st.multiselect(
                "Selecciona los libros a prestar:",
                options=list(diccionario_libros.keys()),
                format_func=lambda x: diccionario_libros[x]
            )
            submit = st.form_submit_button("Registrar Préstamo")
            
            if submit:
                if not codigo_solicitante or not isbn_seleccionados:
                    st.error("Debes ingresar el código del solicitante y seleccionar al menos un libro.")
                else:
                    limite_libros = 5 if tipo_solicitante == "Alumno" else 10
                    if len(isbn_seleccionados) > limite_libros:
                        st.error(f"Un {tipo_solicitante} solo puede llevar un máximo de {limite_libros} libros.")
                    else:
                        dias_prestamo = 7 if tipo_solicitante == "Alumno" else 14
                        fecha_limite = fecha_prestamo + datetime.timedelta(days=dias_prestamo)
                        codigo_limpio = codigo_solicitante.split('|')[0]
                        codigo_alumno = codigo_limpio if tipo_solicitante == "Alumno" else None
                        codigo_profesor = codigo_limpio if tipo_solicitante == "Profesor" else None

                        errores = 0
                        for item in isbn_seleccionados:
                            isbn,ejemplar = item.split('|')
                            exito = registrar_prestamo(
                                isbn_libro=isbn,
                                ejemplar_libro=int(ejemplar),
                                codigo_empleado=codigo_empleado_real,
                                codigo_alumno=codigo_alumno,
                                codigo_profesor=codigo_profesor,
                                fecha_prestamo=fecha_prestamo,
                                fecha_entrega_limite=fecha_limite,
                                estatus='Activo',
                                multa=0.00
                            )
                            if not exito:
                                errores+=1
                        if errores == 0:
                            st.success(f"Préstamo registrado con éxito. Fecha límite de entrega: {fecha_limite.strftime('%d/%m/%Y')}")
                        else:
                            st.error(f"Ocurrieron {errores} al registrar los libros del préstamo en la base de datos")    