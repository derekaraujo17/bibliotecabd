from dotenv import load_dotenv
import streamlit as st
from login import mostrar_login
from principal import mostrar_principal
from menuadmin import mostrar_menu_admin
from database import inicializar_tablas
from menuadminalumno import mostrar_menu_admin_alumno
from menuadminprofesor import mostrar_menu_admin_profesor
load_dotenv()
inicializar_tablas()
st.set_page_config(page_title="Biblioteca", layout="wide")

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None
if "rol" not in st.session_state:
    st.session_state["rol"] = None

if "pantalla_actual" not in st.session_state:
    st.session_state["pantalla_actual"] = "login"

if st.session_state["pantalla_actual"] == "login":
    mostrar_login()
elif st.session_state["pantalla_actual"] == "principal":
    mostrar_principal()
elif st.session_state["pantalla_actual"] == "menuadmin":
    mostrar_menu_admin()
elif st.session_state["pantalla_actual"] == "menuadminalumno":
    mostrar_menu_admin_alumno()
elif st.session_state["pantalla_actual"] == "menuadminprofesor":
    mostrar_menu_admin_profesor()