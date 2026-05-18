import streamlit as st
import base64
import os
import smtplib
from email.message import EmailMessage

def obtener_imagen_base64(nombre_archivo):
    ruta_actual = os.path.dirname(__file__)
    ruta_completa = os.path.join(ruta_actual, nombre_archivo)    
    _, extension = os.path.splitext(ruta_completa)
    ext = extension.lower().replace(".", "")
    tipo_mime = "jpeg" if ext in ["jpg", "jpeg"] else ext
    if not tipo_mime: tipo_mime = "png"

    try:
        with open(ruta_completa, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/{tipo_mime};base64,{encoded_string}"
    except FileNotFoundError:
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

def render_header():
    try:
        ruta_css = os.path.join(os.path.dirname(__file__), "estilosGlobales.css")
        with open(ruta_css, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

    img_b64 = obtener_imagen_base64("buhobliotecalogo.png") 

    usuario_actual = st.session_state.get("usuario", "Invitado")
    if usuario_actual:
        usuario_actual = usuario_actual.upper()

    st.markdown(f"""
    <div class="custom-header"><img src="{img_b64}" class="logo" alt="Logo Biblioteca"><span class="title">Buhoblioteca</span><div class="user-info">Logueado como: <b>{usuario_actual}</b></div></div><div class="espacio-contenido"></div>""", unsafe_allow_html=True)

def enviar_correo_multa(correo_destino, ruta_pdf):
    remitente = os.getenv("EMAIL_USER") 
    password = os.getenv("EMAIL_PASS")  

    msg = EmailMessage()
    msg['Subject'] = 'Aviso de Multa - Buhoblioteca'
    msg['From'] = remitente
    msg['To'] = correo_destino
    
    cuerpo = """
    Estimado usuario,
    
    Adjunto a este correo encontrará el recibo detallado de la multa generada 
    por la devolución tardía del material bibliográfico.
    
    Atentamente,
    Administración de Buhoblioteca.
    """
    msg.set_content(cuerpo)

    try:
        with open(ruta_pdf, 'rb') as f:
            pdf_data = f.read()
        
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='multa.pdf')
    except FileNotFoundError:
        print("Error: No se encontró el archivo PDF para adjuntar.")
        return False

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remitente, password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False