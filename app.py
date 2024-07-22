import streamlit as st
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from num2words import num2words

# Definir la clase PDF con la biblioteca fpdf2
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Oferta de Préstamo', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

# Función para sanitizar el texto y evitar problemas de codificación
def sanitize_text(text):
    return str(text).encode('latin1', 'replace').decode('latin1')

# Función para convertir números en texto en español
def number_to_text(number):
    return num2words(number, lang='es').replace('-', ' ').capitalize()

# Función genérica para generar PDFs a partir de una plantilla
def generate_pdf(template, placeholders):
    pdf = PDF()
    pdf.add_page()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    
    with open(template, 'r', encoding='latin1') as file:
        body = file.read()
    
    for placeholder, value in placeholders.items():
        body = body.replace(placeholder, sanitize_text(value))

    pdf.chapter_body(body)
    return pdf.output(dest='S').encode('latin1')

# Funciones específicas para cada tipo de préstamo
def generate_pdf_cohen_tomador(placeholders):
    template = '/mnt/data/MODELO A - Cohen SA - Oferta de préstamo de VN - COHEN TOMADOR.docx'
    return generate_pdf(template, placeholders)

def generate_pdf_cohen_prestamista(placeholders):
    template = '/mnt/data/MODELO B - Cohen SA - Oferta de préstamo de VN - COHEN PRESTAMISTA.docx'
    return generate_pdf(template, placeholders)

def generate_pdf_cohen_tomador_tbills(placeholders):
    template = '/mnt/data/MODELO C - Cohen SA - Oferta de préstamo de VN - COHEN TOMADOR T-BILLS.docx'
    return generate_pdf(template, placeholders)

def generate_pdf_cohen_prestamista_tbills(placeholders):
    template = '/mnt/data/MODELO D - Cohen SA - Oferta de préstamo de VN - COHEN PRESTAMISTA T-BILLS.docx'
    return generate_pdf(template, placeholders)

def generate_pdf_prestamo_entre_clientes(placeholders):
    template = '/mnt/data/MODELO E - Clientes - Oferta de préstamo de VN- PRESTAMO ENTRE CLIENTES.docx'
    return generate_pdf(template, placeholders)

def generate_pdf_prestamo_entre_clientes_tbills(placeholders):
    template = '/mnt/data/MODELO F - Clientes - Oferta de préstamo de VN - PRESTAMO ENTRE CLIENTES T-BILLS.docx'
    return generate_pdf(template, placeholders)

# Función para enviar el correo electrónico con el PDF adjunto
def enviar_email(pdf_data, filename):
    usuario_smtp = 'gallo@cohen.com.ar'
    contrasena_smtp = 'Cambiar21!'

    mensaje = MIMEMultipart()
    mensaje['From'] = usuario_smtp
    mensaje['To'] = 'ddjj@cohen.com.ar'
    mensaje['Subject'] = 'Oferta de Préstamo'

    adjunto = MIMEBase('application', 'octet-stream')
    adjunto.set_payload(pdf_data)
    encoders.encode_base64(adjunto)
    adjunto.add_header('Content-Disposition', f'attachment; filename={filename}')
    mensaje.attach(adjunto)

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(usuario_smtp, contrasena_smtp)
        servidor.sendmail(usuario_smtp, 'ddjj@cohen.com.ar', mensaje.as_string())
        servidor.quit()
        st.success('Correo enviado exitosamente')
    except Exception as e:
        st.error(f'Error al enviar el correo: {e}')

# Interfaz de usuario con Streamlit
st.title('Generador de Ofertas de Préstamo')
tipo_prestamo = st.selectbox('Tipo de Préstamo', ['COHEN TOMADOR', 'COHEN PRESTAMISTA', 'COHEN TOMADOR T-BILLS', 'COHEN PRESTAMISTA T-BILLS', 'PRESTAMO ENTRE CLIENTES', 'PRESTAMO ENTRE CLIENTES T-BILLS'])

mes = st.text_input('Mes')
dia = st.text_input('Día')
prestamista = st.text_input('Prestamista')
tomador = st.text_input('Tomador')
cuit_prestamista = st.text_input('CUIT Prestamista')
cuit_tomador = st.text_input('CUIT Tomador')
domicilio_prestamista = st.text_input('Domicilio Prestamista')
domicilio_tomador = st.text_input('Domicilio Tomador')
especie = st.text_input('Especie')
valor_nominal = st.number_input('Valor Nominal', min_value=0)
tasa_anual = st.number_input('Tasa Anual (%)', min_value=0.0, format="%.2f")
plazo = st.number_input('Plazo (meses)', min_value=0)
tasa_penalidad = st.number_input('Tasa de Penalidad (%)', min_value=0.0, format="%.2f")

if st.button('Generar PDF'):
    placeholders = {
        '[MES]': mes,
        '[DIA]': dia,
        '[CLIENTE]': prestamista,
        '[TOMADOR]': tomador,
        '[CUITPRESTAMISTA]': cuit_prestamista,
        '[CUITTOMADOR]': cuit_tomador,
        '[DOMICILIOPRESTAMISTA]': domicilio_prestamista,
        '[DOMICILIOTOMADOR]': domicilio_tomador,
        '[ESPECIE]': especie,
        '[VALORNOMINAL]': str(valor_nominal),
        '[VALORNOMINALTEXTO]': number_to_text(valor_nominal),
        '[TASAANUAL]': str(tasa_anual),
        '[PLAZO]': str(plazo),
        '[PLAZOTEXTO]': number_to_text(plazo),
        '[TASAPENALIDAD]': str(tasa_penalidad)
    }

    pdf_data = None
    filename = ''

    if tipo_prestamo == 'COHEN TOMADOR':
        filename = 'oferta_prestamo_cohen_tomador.pdf'
        pdf_data = generate_pdf_cohen_tomador(placeholders)
    elif tipo_prestamo == 'COHEN PRESTAMISTA':
        filename = 'oferta_prestamo_cohen_prestamista.pdf'
        pdf_data = generate_pdf_cohen_prestamista(placeholders)
    elif tipo_prestamo == 'COHEN TOMADOR T-BILLS':
        filename = 'oferta_prestamo_cohen_tomador_tbills.pdf'
        pdf_data = generate_pdf_cohen_tomador_tbills(placeholders)
    elif tipo_prestamo == 'COHEN PRESTAMISTA T-BILLS':
        filename = 'oferta_prestamo_cohen_prestamista_tbills.pdf'
        pdf_data = generate_pdf_cohen_prestamista_tbills(placeholders)
    elif tipo_prestamo == 'PRESTAMO ENTRE CLIENTES':
        filename = 'oferta_prestamo_entre_clientes.pdf'
        pdf_data = generate_pdf_prestamo_entre_clientes(placeholders)
    elif tipo_prestamo == 'PRESTAMO ENTRE CLIENTES T-BILLS':
        filename = 'oferta_prestamo_entre_clientes_tbills.pdf'
        pdf_data = generate_pdf_prestamo_entre_clientes_tbills(placeholders)

    if pdf_data:
        st.download_button('Descargar PDF', pdf_data, file_name=filename)
        enviar_email(pdf_data, filename)
