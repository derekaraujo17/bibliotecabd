import streamlit as st
from helpers import render_header
from database import registrar_libros,obtener_libros
import pandas as pd
from datetime import date

def mostrar_menu_libros():
    render_header()
    col1,col2 = st.columns([3,1])
    with col2:
        if st.button("⬅ Volver al Panel Principal"):
            st.session_state["pantalla_actual"] = "principal"
            st.rerun()
    st.markdown("<h2 style='text-align:center;'>Menú LIBROS</h2>",unsafe_allow_html=True)
    st.divider()
    opcion = st.selectbox("Selecciona una opción:",
                              ["---","Registrar","Consulta individual","Consulta General","Cambiar","Eliminar"])
    if opcion == "Registrar":
        st.subheader("Alta de Libros")
        with st.form("registro_libros",clear_on_submit=True):
            col_a,col_b = st.columns(2)
            with col_a:
                ISBN = st.text_input("ISBN")
                titulo = st.text_input("Título")
                autores = st.text_input("Autor(es)")
            with col_b:
                editorial = st.text_input("Editorial")
                anio_publicacion = st.text_input("Año de Publicación")
                num_ejemplar = st.text_input("Num. ejemplar")
            submit = st.form_submit_button("Guardar Libro")
                
            if submit:
                if not ISBN or not titulo or not autores or not editorial or not anio_publicacion or not num_ejemplar:
                    st.warning("Por favor, completa todos los campos antes de guardar.")
                else:
                    exito = registrar_libros(ISBN, titulo, autores, editorial, anio_publicacion, num_ejemplar)
                    if exito:
                        st.success(f"Libro '{titulo}' (ejemplar {num_ejemplar}) registrado correctamente.")
                    else:
                        st.error("Error al registrar en la base de datos. Verifica que el ISBN no esté repetido.")
    elif opcion == "Consulta General":
        st.subheader("Direcctorio General de Libros")
        datos, columnas = obtener_libros()
        if datos:
            df_libros = pd.DataFrame(datos, columns=columnas)
            st.dataframe(df_libros, use_container_width=True, hide_index=True)
        else:
            st.info("Actualmente no hay libros registrados en la base de datos.")