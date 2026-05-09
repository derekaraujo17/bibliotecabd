import streamlit as st
from helpers import render_header

def mostrar_principal():
    render_header()

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Cerrar sesión"):
            st.session_state["logueado"] = False
            st.session_state["usuario"] = None
            st.session_state["rol"] = None
            st.session_state["pantalla_actual"] = "login"
            st.rerun()

    st.divider()
    st.markdown("<h2 style='text-align: center;'>Panel Principal</h2>", unsafe_allow_html=True)
    
    if st.session_state['rol'] == 'admin':
        st.write("¿A dónde deseas ir?")
        
        if st.button("Gestión de Empleados (Paso 8) ➔"):
            st.session_state["pantalla_actual"] = "menuadmin"
            st.rerun()