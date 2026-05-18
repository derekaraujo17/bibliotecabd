import streamlit as st
from helpers import render_header,enviar_correo_multa
from database import registrar_prestamo,obtener_libros_disponibles,obtener_alumnos,obtener_profesores,obtener_prestamos,obtener_prestamos_activos,procesar_devolucion
import pandas as pd
import datetime

def mostrar_menu_prestamos():
    render_header()
    col1,col2 = st.columns([3,1])
    with col2:
        if st.button("⬅ Volver al Panel Principal"):
            st.session_state["pantalla_actual"] = "principal"
            st.rerun()
    st.markdown("<h2 style='text-align:center;'>Menú PRÉSTAMOS</h2>",unsafe_allow_html=True)
    st.divider()
    opcion = st.selectbox("Selecciona una opción:",
                          ["---","Registrar préstamo","Devolver préstamo","Consulta de préstamo","Consultas de préstamos"])
    if opcion == "Registrar préstamo":
        st.subheader("Registro de préstamos")
        libros_bd, columnas = obtener_libros_disponibles()
        if not libros_bd:
            st.warning("No hay libros registrados en el catálogo aún.")
            return
        diccionario_libros = {
            f"{libro[0]}|{libro[5]}": f"{libro[1]} - Ejemplar: {libro[5]} (ISBN: {libro[0]})" 
            for libro in libros_bd
        }
        alumnos_bd,columnas = obtener_alumnos()
        diccionario_alumnos = {
            f"{alumno[0]}|{alumno[1]}": f"{alumno[0]} - {alumno[1]}"
            for alumno in alumnos_bd
        }
        profesores_bd,columnas = obtener_profesores()
        diccionario_profesores = {
            f"{profesor[0]}|{profesor[1]}": f"{profesor[0]} - {profesor[1]}"
            for profesor in profesores_bd
        }
        codigo_empleado_real = st.session_state.get("codigo_empleado")
        nombre_usuario_actual = st.session_state.get("usuario","")
        tipo_solicitante = st.radio("¿Quién solicita el préstamo?", ["Alumno","Profesor"],horizontal=True)

        with st.form("registro_prestamos",clear_on_submit=True):
            col_a,col_b = st.columns(2)
            with col_a:
                if tipo_solicitante == "Alumno":
                    codigo_solicitante = st.selectbox(
                        "Selecciona el código del alumno:",
                        options=list(diccionario_alumnos.keys()),
                        format_func=lambda x: diccionario_alumnos[x]
                    )
                else:
                    codigo_solicitante = st.selectbox(
                        "Selecciona el código del profesor:",
                        options=list(diccionario_profesores.keys()),
                        format_func=lambda x: diccionario_profesores[x]
                    )
                st.text_input("Código del Empleado que registra",value=str(codigo_empleado_real),disabled=True)
            with col_b:
                fecha_prestamo = st.date_input("Fecha del préstamo",
                                               min_value=datetime.date(2020,1,1),
                                               max_value=datetime.date.today(),
                                               format="DD/MM/YYYY")    
            isbn_seleccionados = st.multiselect(
                "Selecciona los libros a prestar:",
                options=list(diccionario_libros.keys()),
                format_func=lambda x: diccionario_libros[x]
            )
            submit = st.form_submit_button("Registrar Préstamo")
            
            if submit:
                if not codigo_solicitante or not isbn_seleccionados:
                    st.error("Debes ingresar el código del solicitante y seleccionar al menos un libro.")
                else:
                    limite_libros = 5 if tipo_solicitante == "Alumno" else 10
                    if len(isbn_seleccionados) > limite_libros:
                        st.error(f"Un {tipo_solicitante} solo puede llevar un máximo de {limite_libros} libros.")
                    else:
                        dias_prestamo = 7 if tipo_solicitante == "Alumno" else 14
                        fecha_limite = fecha_prestamo + datetime.timedelta(days=dias_prestamo)
                        codigo_limpio = codigo_solicitante.split('|')[0]
                        codigo_alumno = codigo_limpio if tipo_solicitante == "Alumno" else None
                        codigo_profesor = codigo_limpio if tipo_solicitante == "Profesor" else None

                        errores = 0
                        for item in isbn_seleccionados:
                            isbn,ejemplar = item.split('|')
                            exito = registrar_prestamo(
                                isbn_libro=isbn,
                                ejemplar_libro=int(ejemplar),
                                codigo_empleado=codigo_empleado_real,
                                codigo_alumno=codigo_alumno,
                                codigo_profesor=codigo_profesor,
                                fecha_prestamo=fecha_prestamo,
                                fecha_entrega_limite=fecha_limite,
                                estatus='Activo',
                                multa=0.00
                            )
                            if not exito:
                                errores+=1
                        if errores == 0:
                            st.success(f"Préstamo registrado con éxito. Fecha límite de entrega: {fecha_limite.strftime('%d/%m/%Y')}")
                        else:
                            st.error(f"Ocurrieron {errores} al registrar los libros del préstamo en la base de datos")    
    
    elif opcion == "Consultas de préstamos":
        st.subheader("Direcctorio general de préstamos")
        datos,columnas = obtener_prestamos()
        if datos:
            df_prestamos = pd.DataFrame(datos,columns=columnas)
            st.dataframe(df_prestamos, use_container_width=True,hide_index=True)
        else:
            st.info("Actualmente no hay préstamos registrados en la base de datos.")

    elif opcion == "Devolver préstamo":
        st.subheader("Devolución de libros")
        prestamos_activos = obtener_prestamos_activos()
        if not prestamos_activos:
            st.info("No hay préstamos activos en este momento.")
            return
        
        diccionario_prestamos = {
            p[0]: f"Folio {p[0]} - {p[1]} (Libro: {p[2]} | Ejemplar: {p[3]})"
            for p in prestamos_activos
        }

        codigo_seleccionado = st.selectbox(
            "Selecciona el préstamo a devolver:",
            options=list(diccionario_prestamos.keys()),
            format_func=lambda x: diccionario_prestamos[x]
        )

        prestamo_actual = next(p for p in prestamos_activos if p[0] == codigo_seleccionado)
        nombre_sol = prestamo_actual[1]
        titulo_lib = prestamo_actual[2]
        ejemplar_lib = prestamo_actual[3]
        fecha_limite = prestamo_actual[4]
        tipo_sol = prestamo_actual[5]
        correo_sol = prestamo_actual[6]

        st.write(f"**Fecha límite estipulada:** {fecha_limite.strftime('%d/%m/%Y')}")
        with st.form("form_devolucion"):
            fecha_devolucion = st.date_input("Fecha real de devolución:",value=datetime.date.today(),format="DD/MM/YYYY")
            submit_devolucion = st.form_submit_button("Confirmar devolución")

        if submit_devolucion:
            diferencia_dias = (fecha_devolucion - fecha_limite).days
            multa_total = 0.00
            dias_retraso = 0
            if diferencia_dias > 0:
                dias_retraso = diferencia_dias
                tarifa = 5 if tipo_sol == 'Alumno' else 10
                multa_total = dias_retraso * tarifa
                st.warning(f"El préstamo se devolvió con {dias_retraso} días de retraso. Multa generada: ${multa_total}")
            else:
                st.success("Préstamo devuelto a tiempo. No hay multas.")
                
            exito = procesar_devolucion(codigo_seleccionado,fecha_devolucion,multa_total)

            if exito:
                st.success("¡Devolución registrada correctamente en el sistema!")
                if multa_total > 0:
                    titulo_completo = f"{titulo_lib} (Ej. {ejemplar_lib})"
                    from generadorpdf import generar_recibo_multa
                    archivo_pdf = generar_recibo_multa(nombre_sol,titulo_completo,dias_retraso,multa_total)
                    st.info("Generando archivo PDF de la multa...")
                    if correo_sol:
                        with st.spinner("Enviando el correo al usuario..."):
                            correo_enviado = enviar_correo_multa(correo_sol,archivo_pdf)
                            if correo_enviado:
                                st.success(f"Correo enviado exitosamente a: {correo_sol}")
                            else:
                                st.error("Ocurrió un problema al enviar el correo. Verifica las credenciales.")
                    with open(archivo_pdf, "rb") as file:
                        st.download_button("Descargar PDF de multa",data=file,file_name=archivo_pdf,mime="application/pdf")
            else:
                st.error("Ocurrió un error al actualizar la base de datos.")