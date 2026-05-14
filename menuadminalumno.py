import streamlit as st
from helpers import render_header
from database import registrar_alumno, obtener_alumnos
import pandas as pd
from datetime import date

def mostrar_menu_admin_alumno():
    render_header()
    col1,col2 = st.columns([3,1])
    with col2:
        if st.button("⬅ Volver al Panel Principal"):
            st.session_state["pantalla_actual"] = "principal"
            st.rerun()
    st.markdown("<h2 style='text-align:center;'>Menú ALUMNOS</h2>",unsafe_allow_html=True)
    st.divider()
    opcion = st.selectbox("Selecciona una opción:",
                              ["---","Registrar","Consulta individual","Consulta General","Cambiar","Eliminar"])
    if opcion == "Registrar":
        st.subheader("Alta de Alumnos")
        with st.form("registro_alumnos",clear_on_submit=True):
            col_a,col_b = st.columns(2)
            with col_a:
                codigo = st.text_input("Código")
                nombre = st.text_input("Nombre Completo")
                carrera = st.text_input("Carrera")
                correo = st.text_input("Correo")
            with col_b:
                direccion = st.text_input("Dirección")
                telefono = st.text_input("Teléfono")
                sexo = st.selectbox("Sexo",["F","M"])
                fecha_nac = st.date_input("Fecha de Nacimiento",
                                              min_value=date(1950,1,1),
                                              max_value=date.today(),
                                              format="DD/MM/YYYY")
            submit = st.form_submit_button("Guardar Alumno")
                
            if submit:
                if not codigo or not nombre or not carrera or not correo or not direccion or not telefono:
                    st.warning("Por favor, completa todos los campos antes de guardar.")
                else:
                    exito = registrar_alumno(codigo,nombre,carrera,correo,direccion,telefono,sexo,fecha_nac)
                    if exito:
                        st.success(f"Alumno '{nombre}' registrado correctamente.")
                    else:
                        st.error("Error al registrar en la base de datos. Verifica que el código o correo no estén repetidos.")
    elif opcion == "Consulta General":
        st.subheader("Direcctorio General de Alumnos")
        datos, columnas = obtener_alumnos()
        if datos:
            df_alumnos = pd.DataFrame(datos, columns=columnas)
            st.dataframe(df_alumnos, use_container_width=True, hide_index=True)
        else:
            st.info("Actualmente no hay alumnos registrados en la base de datos.")