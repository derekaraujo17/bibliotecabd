import streamlit as st
from helpers import render_header
from database import registrar_empleado, obtener_empleados
import pandas as pd

def mostrar_menu_admin():
    render_header()

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("⬅ Volver al Panel Principal"):
            st.session_state["pantalla_actual"] = "principal"
            st.rerun()

    st.markdown("<h2 style='text-align: center;'>Menú EMPLEADOS</h2>", unsafe_allow_html=True)
    st.divider()

    opcion = st.selectbox("Selecciona una opción:", 
                          ["---", "Registrar", "Consulta Individual", "Consulta General", "Cambiar", "Eliminar"])

    if opcion == "Registrar":
        st.subheader("Alta de Empleados")
        
        with st.form("registro_empleados"):
            col_a, col_b = st.columns(2)
            with col_a:
                codigo = st.number_input("Código", step=1, value=0) 
                nombre = st.text_input("Nombre Completo")
                direccion = st.text_input("Dirección")
            with col_b:
                telefono = st.text_input("Teléfono")
                sexo = st.selectbox("Sexo", ["F", "M"])
                fecha_nac = st.date_input("Fecha de Nacimiento")
                turno = st.selectbox("Turno", ["Matutino", "Vespertino"])

            submit = st.form_submit_button("Guardar Empleado")

            if submit:
                exito = registrar_empleado(codigo, nombre, direccion, telefono, sexo, fecha_nac, turno)
                if exito:
                    st.success(f"Empleado '{nombre}' registrado correctamente.")
                else:
                    st.error("Error al registrar en la base de datos.")
    
    elif opcion == "Consulta General":
        st.subheader("Directorio General de Empleados")
        
        datos, columnas = obtener_empleados()
        
        if datos:
            df_empleados = pd.DataFrame(datos, columns=columnas)
            st.dataframe(df_empleados, use_container_width=True, hide_index=True)
        else:
            st.info("Actualmente no hay empleados registrados en la base de datos.")