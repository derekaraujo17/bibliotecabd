import streamlit as st
import base64
import os

def cargar_imagen_local(nombre_archivo):
    ruta_actual = os.path.dirname(__file__)
    ruta_completa = os.path.join(ruta_actual, nombre_archivo)
    
    try:
        with open(ruta_completa, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{encoded_string}"
    except FileNotFoundError:
        return ""

def mostrar_principal():
    col1,col2,col3 = st.columns([1,2,1])
    with col1:
        st.markdown("📚 Leer para aprender")
    with col3:
        st.info(f"Logueado como: **{st.session_state["usuario"].upper()}**")
        if st.button("Cerrar sesión"):
            st.session_state["logueado"] = False
            st.session_state["usuario"] = None
            st.session_state["rol"] = None
            st.session_state["pantalla_actual"] = "login"
            st.rerun()
    st.divider()
    img_biblioteca = cargar_imagen_local("buhobliotecalogo.jpg")
    if img_biblioteca:
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px; border: 2px solid #ccc; padding: 10px;">
                <img src="{img_biblioteca}" width="100%" style="border-radius: 8px;">
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.warning("Agrega una imagen 'biblioteca.jpg' en la carpeta 'bibliotecabd' para verla aquí.")

    st.markdown("<h2 style='text-align: center;'>Bienvenido al Panel de Administración</h2>", unsafe_allow_html=True)
    if st.session_state['rol'] == 'admin':
        st.write("Cargando opciones de administrador...")