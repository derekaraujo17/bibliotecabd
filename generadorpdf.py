from fpdf import FPDF
import os

def generar_recibo_multa(nombre, titulo_libro, dias_retraso, monto_multa):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Buhoblioteca - Recibo de Multa por Retraso", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Estimado(a): {nombre}", ln=True)
    pdf.cell(200, 10, txt=f"Libro devuelto: {titulo_libro}", ln=True)
    pdf.cell(200, 10, txt=f"Días de retraso: {dias_retraso}", ln=True)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(220, 53, 69)
    pdf.cell(200, 10, txt=f"Monto total a pagar: ${monto_multa}.00 MXN", ln=True)
    
    nombre_archivo = f"multa_{nombre.replace(' ', '_')}.pdf"
    pdf.output(nombre_archivo)
    
    return nombre_archivo