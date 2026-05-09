import streamlit as st
import base64
import os

def obtener_imagen_base64(rutaImagen):
    _, extension = os.path.splitext(rutaImagen)
    tipo_mime = "gif" if extension.lower() == ".gif" else "png" 
    try:
        with open(rutaImagen, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/{tipo_mime};base64,{encoded_string}"
    except FileNotFoundError:
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    
def mostrar_login():
    try:
        with open("bibliotecabd/login.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("No se encontró el archivo login.css")

    st.markdown("<h1 class='titulo-login'>BUHOBLIOTECA</h1>", unsafe_allow_html=True)
    
    usuario = st.text_input("Ingresa tu nombre de usuario")
    contrasena = st.text_input("Ingresa tu contraseña", type="password") 

    if st.button("Iniciar Sesión"):
        if usuario == "administrador" and contrasena == "admin123":
            st.session_state["logueado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["rol"] = "admin"
            st.session_state["pantalla_actual"] = "principal"
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
