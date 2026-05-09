from dotenv import load_dotenv
import streamlit as st
from login import mostrar_login
load_dotenv()
st.set_page_config(page_title="Biblioteca", layout="wide")

if "pantalla_actual" not in st.session_state:
    st.session_state["pantalla_actual"] = "login"

if st.session_state["pantalla_actual"] == "login":
    mostrar_login()