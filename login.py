import streamlit as st
import base64
import os
from helpers import render_header
from database import validar_usuario

def mostrar_login():
    try:
        with open("estilosGlobales.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("No se encontró el archivo estilosGlobales.css")
    render_header()
    st.markdown("<h1 class='titulo-login'>Ingresa tus credenciales para ingresar</h1>", unsafe_allow_html=True)
    
    usuario = st.text_input("Ingresa tu nombre de usuario")
    contrasena = st.text_input("Ingresa tu contraseña", type="password") 

    if st.button("Iniciar Sesión"):
        rol_encontrado = validar_usuario(usuario, contrasena)
        if rol_encontrado:
            st.session_state["logueado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["rol"] = rol_encontrado
            st.session_state["pantalla_actual"] = "principal"
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
