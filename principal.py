import streamlit as st
from helpers import render_header


def mostrar_principal():
    render_header()
    rol = st.session_state.get("rol")

    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("Cerrar sesión"):
            st.session_state["logueado"] = False
            st.session_state["usuario"] = None
            st.session_state["rol"] = None
            st.session_state["pantalla_actual"] = "login"
            st.rerun()

    st.markdown("<h2 style='text-align: center; margin-top: -15px;'>Panel Principal</h2>", unsafe_allow_html=True)
    
    if rol == "admin":
        st.write("Bienvenido, administrador")
        if st.button("Gestión de Empleados ➔"):
            st.session_state["pantalla_actual"] = "menuadmin"
            st.rerun()
    elif rol == "empleado":
        st.write("Bienvenido, Staff")
    elif rol == "usuario":
        st.write("Bienvenido, usuario")
    else:
        st.warning("Rol no reconocido")