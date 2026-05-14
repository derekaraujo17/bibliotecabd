import streamlit as st
from helpers import render_header
from database import registrar_profesor, obtener_profesores
import pandas as pd
from datetime import date

def mostrar_menu_admin_profesor():
    render_header()
    col1, col2 = st.columns([3,1])
    with col2:
        if st.button("⬅ Volver al Panel Principal"):
            st.session_state["pantalla_actual"] = "principal"
            st.rerun()
    st.markdown("<h2 style='text-align:center;'>Menú PROFESORES</h2>",unsafe_allow_html=True)
    st.divider()
    opcion = st.selectbox("Selecciona una opción:",
                          ["---","Registrar","Consulta Individual","Consulta General","Cambiar","Eliminar"])
    if opcion == "Registrar":
        st.subheader("Alta de profesores")
        with st.form("registro_profesores", clear_on_submit=True):
            col_a,col_b = st.columns(2)
            with col_a:
                codigo = st.text_input("Código")
                nombre = st.text_input("Nombre Completo")
                direccion = st.text_input("Dirección")
                telefono = st.text_input("Teléfono")
            with col_b:
                sexo = st.selectbox("Sexo",["F","M"])
                fecha_nac = st.date_input("Fecha de Nacimiento",
                                              min_value=date(1950,1,1),
                                              max_value=date.today(),
                                              format="DD/MM/YYYY")
                departamento = st.text_input("Departamento")
                correo = st.text_input("Correo")
            
            submit = st.form_submit_button("Guardar Profesor")
            
            if submit:
                if not codigo or not nombre or not direccion or not telefono or not sexo or not fecha_nac or not departamento or not correo:
                    st.warning("Por favor, completa todos los campos antes de guardar.")
                else:
                    exito = registrar_profesor(codigo,nombre,direccion,telefono,sexo,fecha_nac,departamento,correo)
                    if exito:
                        st.success(f"Profesor '{nombre}' registrado correctamente.")
                    else:
                        st.error("Error al registrar en la base de datos. Verifica que el código o correo no estén repetidos.")
    elif opcion == "Consulta General":
        st.subheader("Direcctorio General de Profesores")
        datos, columnas = obtener_profesores()
        if datos:
            df_profesores = pd.DataFrame(datos, columns=columnas)
            st.dataframe(df_profesores, use_container_width=True, hide_index=True)
        else:
            st.info("Actualmente no hay profesores registrados en la base de datos.")            