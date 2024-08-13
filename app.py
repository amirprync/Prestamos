import streamlit as st
from fpdf import FPDF
from num2words import num2words
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# Definir la clase PDF con la biblioteca fpdf2
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Oferta de Préstamo', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body, 0, 'J')
        self.ln()

# Función para sanitizar el texto y evitar problemas de codificación
def sanitize_text(text):
    return str(text).encode('latin1', 'replace').decode('latin1')

# Función para convertir números en texto en español
def number_to_text(number):
    return num2words(number, lang='es').replace("-", " ").capitalize()

# Función para generar el PDF para COHEN TOMADOR
def generate_pdf_cohen_tomador(mes, dia, moneda, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuit, domicilio, cuenta_bancaria=None):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    body = (f"Ciudad Autónoma de Buenos Aires, {sanitize_text(dia)} de {sanitize_text(mes)} de 2024\n\n"
            f"Sres.\n"
            f"{sanitize_text(prestamista)}\n"
            f"Presente\n\n"
            f"Ref.: Oferta de Préstamo\n\n"
            f"De nuestra mayor consideración:\n"
            f"Conforme a las conversaciones mantenidas, nos dirigimos a {sanitize_text(prestamista)} (en adelante, el 'Prestamista'), a fin de formular con carácter de irrevocable la presente Oferta de Préstamo de Valores Negociables (en adelante, la 'Oferta de Préstamo').\n"
            f"A los efectos de la presente Oferta de Préstamo, el Prestamista y COHEN S.A. (en adelante, el 'Tomador') serán denominados en forma conjunta como las 'Partes'.\n\n"
            f"PRIMERO: El Tomador ofrece al Prestamista realizar un contrato de préstamo bajo el cual el Prestamista entregará al Tomador, en calidad de préstamo, los Valores Negociables que se indican en el Anexo I a la presente Oferta de Préstamo, bajo el cual se establecen los términos y condiciones que regirán dicho contrato.\n\n"
            f"SEGUNDO: En caso que el Prestamista decida aceptar la presente Oferta de Préstamo, las obligaciones y derechos de las Partes serán estrictamente los que resultan del Anexo I adjunto a la presente.\n\n"
            f"TERCERO: La presente Oferta de Préstamo tiene vigencia por el plazo de 5 (cinco) días hábiles, considerándose aceptada si en o antes de dicho plazo, el Prestamista realiza la transferencia de los Valores Negociables a la cuenta comitente del Tomador, conforme se establece en la cláusula PRIMERA del Anexo I adjunto.\n\n"
            f"Atentamente,\n\n"
            f"____________________________\n"
            f"Por COHEN S.A.\n"
            f"Aclaración: Joaquin Cohen\n"
            f"Carácter: Apoderado\n\n"
            f"____________________________\n"
            f"Por COHEN S.A.\n"
            f"Aclaración: Nicolas Parrondo\n"
            f"Carácter: Apoderado\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"ANEXO I\n"
            f"OFERTA DE PRÉSTAMO DE VALORES NEGOCIABLES\n"
            f"En el supuesto de ser aceptada la Oferta de Préstamo en los términos aquí previstos, de la cual la presente forma parte como Anexo I, se entenderá que se ha perfeccionado el siguiente contrato de préstamo (en adelante, el 'Contrato de Préstamo' o el 'Contrato' indistintamente), y tendrá como partes a:\n"
            f"a) {sanitize_text(prestamista)}, CUIT {sanitize_text(cuit)}, con domicilio en {sanitize_text(domicilio)} (en adelante, el 'Prestamista'), por una parte, y\n"
            f"b) por la otra, COHEN S.A., CUIT 30-55854331-7, con domicilio en la calle Ortiz de Ocampo 3302, Módulo IV, piso 2° de la Ciudad Autónoma de Buenos Aires (en adelante, el 'Tomador' y conjuntamente con el Prestamista, las 'Partes').\n\n"
            f"PRIMERA: El Prestamista transfiere al Tomador en calidad de préstamo, los siguientes valores negociables: {sanitize_text(especie)} por un valor nominal de {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}) con el alcance y extensión que se detalla en el Anexo II (en adelante, los 'Valores Negociables').\n\n"
            f"Los Valores Negociables se encuentran depositados en la cuenta comitente {sanitize_text(comitente_prestamista)}, de su titularidad, abierta en COHEN S.A. (en adelante, la 'Cuenta del Prestamista').\n"
            f"El Tomador acepta recibir los Valores Negociables en su cuenta comitente N° {sanitize_text(comitente_tomador)} abierta en COHEN S.A. (Agente de Negociación, Liquidación y Compensación Integral N° 21) (en adelante, la 'Cuenta del Tomador'), obligándose a devolver los Valores Negociables mediante transferencia a la Cuenta del Prestamista y/u otra que éste indicare fehacientemente conforme previsión contemplada en la cláusula NOVENA del presente Anexo. La constancia de débito de dicha transferencia emitida por COHEN S.A. correspondiente a la Cuenta del Prestamista será suficiente recibo del Tomador por la recepción de los Valores Negociables.\n\n"
            f"SEGUNDA: El presente préstamo se establece por un plazo de {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses contados a partir de la transferencia de los Valores Negociables a la Cuenta del Tomador (en adelante, el 'Plazo'). Durante el Plazo, el Prestamista percibirá una tasa de interés equivalente al {sanitize_text(tasa_anual)}% nominal anual que será abonado, en pesos, por el Tomador al vencimiento del Plazo. El interés se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado.\n"
            f"El interés resultante será abonado en pesos desde la Cuenta del Tomador mediante transferencia a la cuenta bancaria de titularidad del Prestamista indicada en el Anexo II.\n")
    
    # Añadir el texto sobre el tipo de cambio si la moneda es "Dólares"
    if moneda == "Dólares" and cuenta_bancaria:
        body += (f"El mismo será calculado de acuerdo al Tipo de Cambio {sanitize_text(cuenta_bancaria)} del día de pago.\n\n")
    
    body += (f"TERCERA: La renovación de la vigencia del Contrato acaecerá de modo automático en ausencia de una notificación de cancelación anticipada conforme la cláusula CUARTA.\n\n"
            f"CUARTA: El Prestamista podrá solicitar la cancelación anticipada del préstamo de los Valores Negociables antes del vencimiento del Plazo, para lo cual deberá notificar por escrito al Tomador con una antelación de 48 horas hábiles a la efectiva fecha de cancelación. En caso de ejercerse tal derecho, el Tomador abonará en forma proporcional el importe de la contraprestación convenida en la cláusula SEGUNDA.\n\n"
            f"QUINTA: El Tomador se obliga a restituir los Valores Negociables al vencimiento del Plazo.\n\n"
            f"SEXTA: El Tomador se compromete a realizar todos aquellos actos necesarios para la conservación de los Valores Negociables, obligándose a restituirlos a la finalización del Plazo en igual cantidad y especie que los recibiera.\n\n"
            f"SÉPTIMA: El Tomador pagará todos los gastos que genere la operatoria objeto del presente Contrato.\n\n"
            f"OCTAVA: Todos los pagos que corresponda percibir por los Valores Negociables dados en préstamo corresponderán al Prestamista. En tal sentido, el Tomador deberá transferirlos a la Cuenta del Prestamista el día hábil posterior a su percepción.\n\n"
            f"\n\n"
            f"\n\n"
            f"NOVENA: La obligación de restituir los Valores Negociables no requiere interpelación judicial o extrajudicial alguna, configurándose su incumplimiento de pleno derecho por el solo incumplimiento material de la obligación de que se trate en la fecha estipulada, dando derecho al Prestamista a considerar vencido el Plazo y exigir la inmediata cancelación del Contrato de Préstamo y de los intereses devengados bajo el mismo.\n\n"
            f"DÉCIMA: El Prestamista asume el riesgo por las oscilaciones propias de los mercados que determinen variaciones de precios y/o cancelaciones de los Valores Negociables.\n\n"
            f"DÉCIMO PRIMERA: El tomador declara conocer que la falta de devolución de los Valores Negociables en tiempo y forma generará una penalidad del {sanitize_text(interes)}% mensual por cada día de retardo en el cumplimiento de su obligación de restituir.\n\n"
            f"DÉCIMO SEGUNDA: Estas operaciones no gozan del sistema de garantía de liquidación de Bolsas y Mercados Argentinos S.A. (BYMA).\n\n"
            f"DÉCIMO TERCERA: El Prestamista no asume ningún tipo de responsabilidad por las situaciones de mercado o incumplimiento por parte del emisor que se pudieran dar en relación a los Valores Negociables mientras se encuentren en poder del Tomador. Asimismo, el Prestamista no garantiza ningún tipo de beneficio económico como consecuencia de la utilización de los mismos.\n\n"
            f"DÉCIMO CUARTA: El Tomador no podrá ceder su posición contractual bajo el Contrato, ni ninguno de los derechos emergentes del mismo sin el consentimiento previo y escrito otorgado por el Prestamista.\n\n"
            f"DÉCIMO QUINTA: Toda modificación a este Contrato deberá ser realizada por las Partes por escrito y conforme las mismas formalidades que se observan en este Contrato.\n\n"
            f"DÉCIMO SEXTA: Para todos los efectos legales derivados de esta Oferta, las Partes constituyen sus domicilios en los indicados en el segundo párrafo del presente Anexo, donde se tendrán por válidas todas las notificaciones. Toda controversia relacionada al presente Contrato será resuelta en forma inapelable por el Tribunal de Arbitraje General de la Bolsa de Comercio de Buenos Aires por las reglas del arbitraje de derecho, que las partes declaran conocer y aceptar.\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\nANEXO II\n"
            f"Condiciones de la operación de Préstamo de Títulos Valores:\n\n"
            f"Prestamista: {sanitize_text(prestamista)}, cuenta Comitente N° {sanitize_text(comitente_prestamista)} Depositante N° {sanitize_text(depositante_prestamista)}.\n\n"
            f"Tomador: {sanitize_text(tomador)}, cuenta comitente N° {sanitize_text(comitente_tomador)} Depositante N° {sanitize_text(depositante_tomador)}.\n\n"
            f"Especie: {sanitize_text(especie)} (código especie {sanitize_text(codigo_especie)}).\n\n"
            f"Valor Nominal: {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}).\n\n"
            f"Tasa: {sanitize_text(tasa_anual)}% nominal anual.\n\n"
            f"Interés: Se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado. Será abonado en pesos desde la Cuenta del Tomador mediante depósito en la Cuenta del Prestamista.\n")

    if moneda == "Dólares" and cuenta_bancaria:
        body += (f"El mismo será calculado de acuerdo al Tipo de Cambio {sanitize_text(cuenta_bancaria)} del día de pago.\n\n")
    
    body += (f"Plazo: {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses.\n\n"
            f"Base de Cálculo: Actual/365.\n")

    pdf.chapter_body(body)
    return pdf.output(dest='S')

# Función para generar el PDF para COHEN PRESTAMISTA
def generate_pdf_cohen_prestamista(mes, dia, moneda, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuit, domicilio, cuenta_bancaria=None):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    body = (f"Ciudad Autónoma de Buenos Aires, {sanitize_text(dia)} de {sanitize_text(mes)} de 2024\n\n"
            f"Sres.\n"
            f"Cohen S.A.\n"
            f"Presente\n\n"
            f"Ref.: Oferta de Préstamo de Valores Negociables\n\n"
            f"De nuestra mayor consideración:\n"
            f"Conforme a las conversaciones mantenidas, nos dirigimos a Cohen S.A. (en adelante, el 'Prestamista'), a fin de formular con carácter de irrevocable la presente Oferta de Préstamo de Valores Negociables (en adelante, la 'Oferta de Préstamo').\n"
            f"A los efectos de la presente Oferta de Préstamo, el Prestamista y {sanitize_text(tomador)} (en adelante, el 'Tomador') serán denominados en forma conjunta como las 'Partes'.\n\n"
            f"PRIMERO: El Tomador ofrece al Prestamista realizar un contrato de préstamo bajo el cual el Prestamista entregará al Tomador, en calidad de préstamo, los Valores Negociables que se indican en el Anexo I a la presente Oferta de Préstamo, bajo el cual se establecen los términos y condiciones que regirán dicho contrato.\n\n"
            f"SEGUNDO: En caso que el Prestamista decida aceptar la presente Oferta de Préstamo, las obligaciones y derechos de las Partes serán estrictamente los que resultan del Anexo I adjunto a la presente.\n\n"
            f"TERCERO: La presente Oferta de Préstamo tiene vigencia por el plazo de 5 (cinco) días hábiles, considerándose aceptada si en o antes de dicho plazo, el Prestamista realiza la transferencia de los Valores Negociables a la cuenta comitente del Tomador, conforme se establece en la cláusula PRIMERA del Anexo I adjunto.\n"
            f"Atentamente,\n\n"
            f"____________________________\n"
            f"Por {sanitize_text(tomador)}\n"
            f"Aclaración:\n"
            f"Carácter:\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"ANEXO I\n"
            f"OFERTA DE PRÉSTAMO DE VALORES NEGOCIABLES\n"
            f"En el supuesto de ser aceptada la Oferta de Préstamo en los términos aquí previstos, de la cual la presente forma parte como Anexo I, se entenderá que se ha perfeccionado el siguiente contrato de préstamo (en adelante, el 'Contrato de Préstamo' o el 'Contrato' indistintamente), y tendrá como partes a:\n"
            f"a) {sanitize_text(tomador)}, CUIT {sanitize_text(cuit)}, con domicilio en {sanitize_text(domicilio)} (en adelante, el 'Tomador'), por una parte, y\n"
            f"b) por la otra, COHEN S.A., CUIT 30-55854331-7, con domicilio en la calle Ortiz de Ocampo 3302, Módulo IV, piso 2° de la Ciudad Autónoma de Buenos Aires (en adelante, el 'Prestamista' y conjuntamente con el Prestamista, las 'Partes').\n\n"
            f"PRIMERA: El Prestamista transfiere al Tomador en calidad de préstamo, los siguientes valores negociables: {sanitize_text(especie)} por un valor nominal de {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}) con el alcance y extensión que se detalla en el Anexo II (en adelante, los 'Valores Negociables').\n"
            f"Los Valores Negociables se encuentran depositados en la cuenta comitente {sanitize_text(comitente_prestamista)}, de su titularidad, abierta en COHEN S.A. (en adelante, la 'Cuenta del Prestamista').\n"
            f"El Tomador acepta recibir los Valores Negociables en su cuenta comitente N° {sanitize_text(comitente_tomador)} abierta en COHEN S.A. (Agente de Negociación, Liquidación y Compensación Integral N° 21) (en adelante, la 'Cuenta del Tomador'), obligándose a devolver los Valores Negociables mediante transferencia a la Cuenta del Prestamista y/u otra que éste indicare fehacientemente conforme previsión contemplada en la cláusula NOVENA del presente Anexo. La constancia de débito de dicha transferencia emitida por COHEN S.A. correspondiente a la Cuenta del Prestamista será suficiente recibo del Tomador por la recepción de los Valores Negociables.\n"
            f"SEGUNDA: El presente préstamo se establece por un plazo de {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses contados a partir de la transferencia de los Valores Negociables a la Cuenta del Tomador (en adelante, el 'Plazo'). Durante el Plazo, el Prestamista percibirá una tasa de interés equivalente al {sanitize_text(tasa_anual)}% nominal anual que será abonado, en pesos, por el Tomador al vencimiento del Plazo. El interés se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado.\n\n"
            f"El interés resultante será abonado en pesos desde la Cuenta del Tomador mediante transferencia a la cuenta bancaria de titularidad del Prestamista indicada en el Anexo II.\n")
    
    if moneda == "Dólares":
        body += (f"El mismo será calculado de acuerdo al Tipo de Cambio {sanitize_text(cuenta_bancaria)} del día de pago.\n\n")
    
    body += (f"TERCERA: La renovación de la vigencia del Contrato acaecerá de modo automático en ausencia de una notificación de cancelación anticipada conforme la cláusula CUARTA.\n\n"
            f"CUARTA: El Prestamista podrá solicitar la cancelación anticipada del préstamo de los Valores Negociables antes del vencimiento del Plazo, para lo cual deberá notificar por escrito al Tomador con una antelación de 48 horas hábiles a la efectiva fecha de cancelación. En caso de ejercerse tal derecho, el Tomador abonará en forma proporcional el importe de la contraprestación convenida en la cláusula SEGUNDA.\n\n"
            f"QUINTA: El Tomador se obliga a restituir los Valores Negociables al vencimiento del Plazo.\n\n"
            f"SEXTA: El Tomador se compromete a realizar todos aquellos actos necesarios para la conservación de los Valores Negociables, obligándose a restituirlos a la finalización del Plazo en igual cantidad y especie que los recibiera.\n\n"
            f"SÉPTIMA: El Tomador pagará todos los gastos que genere la operatoria objeto del presente Contrato.\n\n"
            f"OCTAVA: Todos los pagos que corresponda percibir por los Valores Negociables dados en préstamo corresponderán al Prestamista. En tal sentido, el Tomador deberá transferirlos a la Cuenta del Prestamista el día hábil posterior a su percepción.\n\n"
            f"NOVENA: La obligación de restituir los Valores Negociables no requiere interpelación judicial o extrajudicial alguna, configurándose su incumplimiento de pleno derecho por el solo incumplimiento material de la obligación de que se trate en la fecha estipulada, dando derecho al Prestamista a considerar vencido el Plazo y exigir la inmediata cancelación del Contrato de Préstamo y de los intereses devengados bajo el mismo.\n\n"
            f"DÉCIMA: El tomador declara conocer que la falta de devolución de los Valores Negociables en tiempo y forma generará una penalidad del {sanitize_text(interes)}% mensual por cada día de retardo en el cumplimiento de su obligación de restituir.\n\n"
            f"DÉCIMO PRIMERA: Estas operaciones no gozan del sistema de garantía de liquidación de Bolsas y Mercados Argentinos S.A. (BYMA).\n\n"
            f"DÉCIMO SEGUNDA: El Prestamista no asume ningún tipo de responsabilidad por las situaciones de mercado o incumplimiento por parte del emisor que se pudieran dar en relación a los Valores Negociables mientras se encuentren en poder del Tomador. Asimismo, el Prestamista no garantiza ningún tipo de beneficio económico como consecuencia de la utilización de los mismos.\n\n"
            f"DÉCIMO TERCERA: El Tomador no podrá ceder su posición contractual bajo el Contrato, ni ninguno de los derechos emergentes del mismo sin el consentimiento previo y escrito otorgado por el Prestamista.\n\n"
            f"DÉCIMO CUARTA: Toda modificación a este Contrato deberá ser realizada por las Partes por escrito y conforme las mismas formalidades que se observan en este Contrato.\n\n"
            f"DÉCIMO QUINTA: Para todos los efectos legales derivados de esta Oferta, las Partes constituyen sus domicilios en los indicados en el segundo párrafo del presente Anexo, donde se tendrán por válidas todas las notificaciones. Toda controversia relacionada al presente Contrato será resuelta en forma inapelable por el Tribunal de Arbitraje General de la Bolsa de Comercio de Buenos Aires por las reglas del arbitraje de derecho, que las partes declaran conocer y aceptar.\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"ANEXO II\n\n"
            f"Condiciones de la operación de Préstamo de Títulos Valores:\n"
            f"Prestamista: {sanitize_text(prestamista)}, cuenta Comitente N° {sanitize_text(comitente_prestamista)} Depositante N° {sanitize_text(depositante_prestamista)}.\n"
            f"Tomador: {sanitize_text(tomador)}, cuenta comitente N° {sanitize_text(comitente_tomador)} Depositante N° {sanitize_text(depositante_tomador)}.\n"
            f"Especie: {sanitize_text(especie)} (código especie {sanitize_text(codigo_especie)}).\n"
            f"Valor Nominal: {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}).\n"
            f"Tasa: {sanitize_text(tasa_anual)}% nominal anual.\n"
            f"Interés: Se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado. Será abonado en pesos desde la Cuenta del Tomador mediante depósito en la Cuenta del Prestamista.\n")
    
    if moneda == "Dólares":
        body += (f" El mismo será calculado de acuerdo al Tipo de Cambio {sanitize_text(cuenta_bancaria)} del día de pago.\n")
    
    body += (f"Plazo: {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses.\n"
            f"Base de Cálculo: Actual/365.\n")

    pdf.chapter_body(body)
    return pdf.output(dest='S')

# Función para generar el PDF para COHEN TOMADOR T-BILLS
def generate_pdf_cohen_tomador_tbills(mes, dia, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuenta_bancaria, cuit, domicilio):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    body = (f"Ciudad Autónoma de Buenos Aires, {sanitize_text(dia)} de {sanitize_text(mes)} de 2024\n\n"
            f"Sres.\n"
            f"{sanitize_text(prestamista)}\n"
            f"Presente\n\n"
            f"Ref.: Oferta de Préstamo\n\n"
            f"De nuestra mayor consideración:\n"
            f"Conforme a las conversaciones mantenidas, nos dirigimos a {sanitize_text(prestamista)} (en adelante, el 'Prestamista'), a fin de formular con carácter de irrevocable la presente Oferta de Préstamo de Valores Negociables (en adelante, la 'Oferta de Préstamo').\n"
            f"A los efectos de la presente Oferta de Préstamo, el Prestamista y COHEN S.A. (en adelante, el 'Tomador') serán denominados en forma conjunta como las 'Partes'.\n"
            f"PRIMERO: El Tomador ofrece al Prestamista realizar un contrato de préstamo bajo el cual el Prestamista entregará al Tomador, en calidad de préstamo, los Valores Negociables que se indican en el Anexo I a la presente Oferta de Préstamo, bajo el cual se establecen los términos y condiciones que regirán dicho contrato.\n"
            f"SEGUNDO: En caso que el Prestamista decida aceptar la presente Oferta de Préstamo, las obligaciones y derechos de las Partes serán estrictamente los que resultan del Anexo I adjunto a la presente.\n"
            f"TERCERO: La presente Oferta de Préstamo tiene vigencia por el plazo de 5 (cinco) días hábiles, considerándose aceptada si en o antes de dicho plazo, el Prestamista realiza la transferencia de los Valores Negociables a la cuenta comitente del Tomador, conforme se establece en la cláusula PRIMERA del Anexo I adjunto.\n"
            f"Atentamente,\n\n"
            f"____________________________\n"
            f"Por COHEN S.A.\n"
            f"Aclaración: Joaquin Cohen\n"
            f"Carácter: Apoderado\n\n"
            f"____________________________\n"
            f"Por COHEN S.A.\n"
            f"Aclaración: Nicolas Parrondo\n"
            f"Carácter: Apoderado\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"ANEXO I\n"
            f"OFERTA DE PRÉSTAMO DE VALORES NEGOCIABLES\n"
            f"En el supuesto de ser aceptada la Oferta de Préstamo en los términos aquí previstos, de la cual la presente forma parte como Anexo I, se entenderá que se ha perfeccionado el siguiente contrato de préstamo (en adelante, el 'Contrato de Préstamo' o el 'Contrato' indistintamente), y tendrá como partes a:\n"
            f"a) {sanitize_text(prestamista)}, CUIT {sanitize_text(cuit)}, con domicilio en {sanitize_text(domicilio)} (en adelante, el 'Prestamista'), por una parte, y\n"
            f"b) por la otra, COHEN S.A., CUIT 30-55854331-7, con domicilio en la calle Ortiz de Ocampo 3302, Módulo IV, piso 2° de la Ciudad Autónoma de Buenos Aires (en adelante, el 'Tomador' y conjuntamente con el Prestamista, las 'Partes').\n\n"
            f"PRIMERA: El Prestamista transfiere al Tomador en calidad de préstamo, los siguientes valores negociables: {sanitize_text(especie)} por un valor nominal de {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}) con el alcance y extensión que se detalla en el Anexo II (en adelante, los 'Valores Negociables').\n"
            f"Los Valores Negociables se encuentran depositados en la cuenta comitente {sanitize_text(comitente_prestamista)}, de su titularidad, abierta en COHEN S.A. (en adelante, la 'Cuenta del Prestamista').\n"
            f"El Tomador acepta recibir los Valores Negociables en su cuenta comitente N° {sanitize_text(comitente_tomador)} abierta en COHEN S.A. (Agente de Negociación, Liquidación y Compensación Integral N° 21) (en adelante, la 'Cuenta del Tomador'), obligándose a devolver los Valores Negociables mediante transferencia a la Cuenta del Prestamista y/u otra que éste indicare fehacientemente conforme previsión contemplada en la cláusula NOVENA del presente Anexo. La constancia de débito de dicha transferencia emitida por COHEN S.A. correspondiente a la Cuenta del Prestamista será suficiente recibo del Tomador por la recepción de los Valores Negociables.\n"
            f"SEGUNDA: El presente préstamo se establece por un plazo de {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) mes contados a partir de la transferencia de los Valores Negociables a la Cuenta del Tomador (en adelante, el 'Plazo'). Durante el Plazo, el Prestamista percibirá una tasa de interés equivalente al {sanitize_text(tasa_anual)}% nominal anual que será abonado, en pesos, por el Tomador al vencimiento del Plazo. El interés se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado.\n"
            f"El interés resultante será abonado en pesos desde la Cuenta del Tomador mediante transferencia a la cuenta bancaria de titularidad del Prestamista indicada en el Anexo II. El mismo será calculado de acuerdo al Tipo de Cambio {sanitize_text(cuenta_bancaria)} del día de pago.\n"
            f"TERCERA: La renovación de la vigencia del Contrato acaecerá de modo automático en ausencia de una notificación de cancelación anticipada conforme la cláusula CUARTA.\n"
            f"CUARTA: El Prestamista podrá solicitar la cancelación anticipada del préstamo de los Valores Negociables antes del vencimiento del Plazo, para lo cual deberá notificar por escrito al Tomador con una antelación de 48 horas hábiles a la efectiva fecha de cancelación. En caso de ejercerse tal derecho, el Tomador abonará en forma proporcional el importe de la contraprestación convenida en la cláusula SEGUNDA.\n"
            f"QUINTA: El Tomador se obliga a restituir los Valores Negociables al vencimiento del Plazo.\n"
            f"SEXTA: El Tomador se compromete a realizar todos aquellos actos necesarios para la conservación de los Valores Negociables, obligándose a restituirlos a la finalización del Plazo en igual cantidad a la  que  recibiera.\n"
            f"SÉPTIMA: El Tomador pagará todos los gastos que genere la operatoria objeto del presente Contrato.\n"
            f"OCTAVA: La obligación de restituir los Valores Negociables no requiere interpelación judicial o extrajudicial alguna, configurándose su incumplimiento de pleno derecho por el solo incumplimiento material de la obligación de que se trate en la fecha estipulada, dando derecho al Prestamista a considerar vencido el Plazo y exigir la inmediata cancelación del Contrato de Préstamo y de los intereses devengados bajo el mismo.\n"
            f"NOVENA: El Prestamista asume el riesgo por las oscilaciones propias de los mercados que determinen variaciones de precios y/o cancelaciones de los Valores Negociables.\n"
            f"DÉCIMA: El tomador declara conocer que la falta de devolución de los Valores Negociables en tiempo y forma generará una penalidad del {sanitize_text(interes)}% mensual por cada día de retardo en el cumplimiento de su obligación de restituir.\n"
            f"DÉCIMO PRIMERA: Estas operaciones no gozan del sistema de garantía de liquidación de Bolsas y Mercados Argentinos S.A. (BYMA).\n"
            f"DÉCIMO SEGUNDA: El Prestamista no asume ningún tipo de responsabilidad por las situaciones de mercado o incumplimiento por parte del emisor que se pudieran dar en relación a los Valores Negociables mientras se encuentren en poder del Tomador. Asimismo, el Prestamista no garantiza ningún tipo de beneficio económico como consecuencia de la utilización de los mismos.\n"
            f"DÉCIMO TERCERA: El Tomador no podrá ceder su posición contractual bajo el Contrato, ni ninguno de los derechos emergentes del mismo sin el consentimiento previo y escrito otorgado por el Prestamista.\n"
            f"DÉCIMO CUARTA: Toda modificación a este Contrato deberá ser realizada por las Partes por escrito y conforme las mismas formalidades que se observan en este Contrato.\n"
            f"DÉCIMO QUINTA: Para todos los efectos legales derivados de esta Oferta, las Partes constituyen sus domicilios en los indicados en el segundo párrafo del presente Anexo, donde se tendrán por válidas todas las notificaciones. Toda controversia relacionada al presente Contrato será resuelta en forma inapelable por el Tribunal de Arbitraje General de la Bolsa de Comercio de Buenos Aires por las reglas del arbitraje de derecho, que las partes declaran conocer y aceptar.\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"\n\n"
            f"ANEXO II\n\n"
            f"Condiciones de la operación de Préstamo de Títulos Valores:\n\n"
            f"Prestamista: {sanitize_text(prestamista)}, cuenta Comitente N° {sanitize_text(comitente_prestamista)} Depositante N° {sanitize_text(depositante_prestamista)}.\n\n"
            f"Tomador: {sanitize_text(tomador)}, cuenta comitente N° {sanitize_text(comitente_tomador)} Depositante N° {sanitize_text(depositante_tomador)}.\n\n"
            f"Especie: {sanitize_text(especie)} (código especie {sanitize_text(codigo_especie)}).\n\n"
            f"Valor Nominal: {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}).\n\n"
            f"Tasa: {sanitize_text(tasa_anual)}% nominal anual.\n\n"
            f"Interés: Se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado. Será abonado en pesos desde la Cuenta del Tomador mediante depósito en la Cuenta del Prestamista. El mismo será calculado de acuerdo al Tipo de Cambio {sanitize_text(cuenta_bancaria)} del día de pago.\n\n"
            f"Plazo: {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses.\n\n"
            f"Base de Cálculo: Actual/365.\n")

    pdf.chapter_body(body)
    return pdf.output(dest='S')

# Función para generar el PDF para COHEN PRESTAMISTA T-BILLS
def generate_pdf_cohen_prestamista_tbills(mes, dia, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuenta_bancaria, cuit, domicilio):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    body = (f"Ciudad Autónoma de Buenos Aires, {sanitize_text(dia)} de {sanitize_text(mes)} de 2024\n\n"
            f"Sres.\n"
            f"Cohen S.A.\n"
            f"Presente\n\n"
            f"Ref.: Oferta de Préstamo de Valores Negociables\n\n"
            f"De nuestra mayor consideración:\n"
            f"Conforme a las conversaciones mantenidas, nos dirigimos a Cohen S.A. (en adelante, el 'Prestamista'), a fin de formular con carácter de irrevocable la presente Oferta de Préstamo de Valores Negociables (en adelante, la 'Oferta de Préstamo').\n"
            f"A los efectos de la presente Oferta de Préstamo, el Prestamista y {sanitize_text(tomador)} (en adelante, el 'Tomador') serán denominados en forma conjunta como las 'Partes'.\n\n"
            f"PRIMERO: El Tomador ofrece al Prestamista realizar un contrato de préstamo bajo el cual el Prestamista entregará al Tomador, en calidad de préstamo, los Valores Negociables que se indican en el Anexo I a la presente Oferta de Préstamo, bajo el cual se establecen los términos y condiciones que regirán dicho contrato.\n\n"
            f"SEGUNDO: En caso que el Prestamista decida aceptar la presente Oferta de Préstamo, las obligaciones y derechos de las Partes serán estrictamente los que resultan del Anexo I adjunto a la presente.\n\n"
            f"TERCERO: La presente Oferta de Préstamo tiene vigencia por el plazo de 5 (cinco) días hábiles, el Prestamista realiza la transferencia de los Valores Negociables a la cuenta comitente del Tomador, conforme se establece en la cláusula PRIMERA del Anexo I adjunto.\n\n"
            f"Atentamente,\n\n"
            f"____________________________\n"
            f"Por {sanitize_text(tomador)}\n"
            f"Aclaración:\n"
            f"Carácter:\n\n"
            f"ANEXO I\n"
            f"OFERTA DE PRÉSTAMO DE VALORES NEGOCIABLES\n"
            f"En el supuesto de ser aceptada la Oferta de Préstamo en los términos aquí previstos, de la cual la presente forma parte como Anexo I, se entenderá que se ha perfeccionado el siguiente contrato de préstamo (en adelante, el 'Contrato de Préstamo' o el 'Contrato' indistintamente), y tendrá como partes a:\n"
            f"a) {sanitize_text(prestamista)}, CUIT {sanitize_text(cuit)}, con domicilio en {sanitize_text(domicilio)} (en adelante, el 'Tomador'), por una parte, y\n"
            f"b) por la otra, COHEN S.A., CUIT 30-55854331-7, con domicilio en la calle Ortiz de Ocampo 3302, Módulo IV, piso 2° de la Ciudad Autónoma de Buenos Aires (en adelante, el 'Prestamista' y conjuntamente con el Prestamista, las 'Partes').\n\n"
            f"PRIMERA: El Prestamista transfiere al Tomador en calidad de préstamo, los siguientes valores negociables: {sanitize_text(especie)} por un valor nominal de {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}) con el alcance y extensión que se detalla en el Anexo II (en adelante, los 'Valores Negociables').\n\n"
            f"Los Valores Negociables se encuentran depositados en la cuenta comitente {sanitize_text(comitente_prestamista)}, de su titularidad, abierta en COHEN S.A. (en adelante, la 'Cuenta del Prestamista').\n"
            f"El Tomador acepta recibir los Valores Negociables en su cuenta comitente N° {sanitize_text(comitente_tomador)} abierta en COHEN S.A. (Agente de Negociación, Liquidación y Compensación Integral N° 21) (en adelante, la 'Cuenta del Tomador'), obligándose a devolver los Valores Negociables mediante transferencia a la Cuenta del Prestamista y/u otra que éste indicare fehacientemente conforme previsión contemplada en la cláusula NOVENA del presente Anexo. La constancia de débito de dicha transferencia emitida por COHEN S.A. correspondiente a la Cuenta del Prestamista será suficiente recibo del Tomador por la recepción de los Valores Negociables.\n\n"
            f"SEGUNDA: El presente préstamo se establece por un plazo de {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses contados a partir de la transferencia de los Valores Negociables a la Cuenta del Tomador (en adelante, el 'Plazo'). Durante el Plazo, el Prestamista percibirá una tasa de interés equivalente al {sanitize_text(tasa_anual)}% nominal anual que será abonado, en pesos, por el Tomador al vencimiento del Plazo. El interés se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado.\n\n"
            f"El interés resultante será abonado en pesos desde la Cuenta del Tomador mediante transferencia a la cuenta bancaria de titularidad del Prestamista indicada en el Anexo II. El mismo será calculado de acuerdo al Tipo de Cambio {sanitize_text(cuenta_bancaria)} del día de pago.\n\n"
            f"TERCERA: La renovación de la vigencia del Contrato acaecerá de modo automático en ausencia de una notificación de cancelación anticipada conforme la cláusula CUARTA.\n\n"
            f"CUARTA: El Prestamista podrá solicitar la cancelación anticipada del préstamo de los Valores Negociables antes del vencimiento del Plazo, para lo cual deberá notificar por escrito al Tomador con una antelación de 48 horas hábiles a la efectiva fecha de cancelación. En caso de ejercerse tal derecho, el Tomador abonará en forma proporcional el importe de la contraprestación convenida en la cláusula SEGUNDA.\n\n"
            f"QUINTA: El Tomador se obliga a restituir los Valores Negociables al vencimiento del Plazo.\n\n"
            f"SEXTA: El Tomador se compromete a realizar todos aquellos actos necesarios para la conservación de los Valores Negociables, obligándose a restituirlos a la finalización del Plazo en igual cantidad a la que los recibiera.\n\n"
            f"SÉPTIMA: El Tomador pagará todos los gastos que genere la operatoria objeto del presente Contrato.\n\n"
            f"OCTAVA: La obligación de restituir los Valores Negociables no requiere interpelación judicial o extrajudicial alguna, configurándose su incumplimiento de pleno derecho por el solo incumplimiento material de la obligación de que se trate en la fecha estipulada, dando derecho al Prestamista a considerar vencido el Plazo y exigir la inmediata cancelación del Contrato de Préstamo y de los intereses devengados bajo el mismo.\n\n"
            f"NOVENA: El tomador declara conocer que la falta de devolución de los Valores Negociables en tiempo y forma generará una penalidad del {sanitize_text(interes)}% mensual por cada día de retardo en el cumplimiento de su obligación de restituir.\n\n"
            f"DÉCIMA: Estas operaciones no gozan del sistema de garantía de liquidación de Bolsas y Mercados Argentinos S.A. (BYMA).\n\n"
            f"DÉCIMO PRIMERA: El Prestamista no asume ningún tipo de responsabilidad por las situaciones de mercado o incumplimiento por parte del emisor que se pudieran dar en relación a los Valores Negociables mientras se encuentren en poder del Tomador. Asimismo, el Prestamista no garantiza ningún tipo de beneficio económico como consecuencia de la utilización de los mismos.\n\n"
            f"DÉCIMO SEGUNDA: El Tomador no podrá ceder su posición contractual bajo el Contrato, ni ninguno de los derechos emergentes del mismo sin el consentimiento previo y escrito otorgado por el Prestamista.\n\n"
            f"DÉCIMO TERCERA: Toda modificación a este Contrato deberá ser realizada por las Partes por escrito y conforme las mismas formalidades que se observan en este Contrato.\n\n"
            f"DÉCIMO CUARTA: Para todos los efectos legales derivados de esta Oferta, las Partes constituyen sus domicilios en los indicados en el segundo párrafo del presente Anexo, donde se tendrán por válidas todas las notificaciones. Toda controversia relacionada al presente Contrato será resuelta en forma inapelable por el Tribunal de Arbitraje General de la Bolsa de Comercio de Buenos Aires por las reglas del arbitraje de derecho, que las partes declaran conocer y aceptar.\n\n"
            f"\nANEXO II\n"
            f"Condiciones de la operación de Préstamo de Títulos Valores:\n\n"
            f"Prestamista: {sanitize_text(prestamista)}, cuenta Comitente N° {sanitize_text(comitente_prestamista)} Depositante N° {sanitize_text(depositante_prestamista)}.\n\n"
            f"Tomador: {sanitize_text(tomador)}, cuenta comitente N° {sanitize_text(comitente_tomador)} Depositante N° {sanitize_text(depositante_tomador)}.\n\n"
            f"Especie: {sanitize_text(especie)} (código especie {sanitize_text(codigo_especie)}).\n\n"
            f"Valor Nominal: {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}).\n\n"
            f"Tasa: {sanitize_text(tasa_anual)}% nominal anual.\n\n"
            f"Interés: Se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado. Será abonado en pesos desde la Cuenta del Tomador mediante depósito en la Cuenta del Prestamista. El mismo será calculado de acuerdo al Tipo de Cambio {sanitize_text(cuenta_bancaria)} del día de pago.\n\n"
            f"Plazo: {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses.\n\n"
            f"Base de Cálculo: Actual/365.\n")

    pdf.chapter_body(body)
    return pdf.output(dest='S')

# Función para generar el PDF para PRESTAMO ENTRE CLIENTES
def generate_pdf_prestamo_entre_clientes(mes, dia, moneda, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuit_prestamista, domicilio_prestamista, cuit_tomador, domicilio_tomador, cuenta_bancaria=None):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    body = (f"Ciudad Autónoma de Buenos Aires, {sanitize_text(dia)} de {sanitize_text(mes)} de 2024\n\n"
            f"Sres.\n"
            f"{sanitize_text(prestamista)}\n"
            f"Presente\n\n"
            f"Ref.: Oferta de Préstamo\n\n"
            f"De nuestra mayor consideración:\n"
            f"Conforme a las conversaciones mantenidas, nos dirigimos a {sanitize_text(prestamista)} (en adelante, el 'Prestamista'), a fin de formular con carácter de irrevocable la presente Oferta de Préstamo de Valores Negociables (en adelante, la 'Oferta de Préstamo').\n"
            f"A los efectos de la presente Oferta de Préstamo, el Prestamista y {sanitize_text(tomador)} (en adelante, el 'Tomador') serán denominados en forma conjunta como las 'Partes'.\n\n"
            f"PRIMERO: El Tomador ofrece al Prestamista realizar un contrato de préstamo bajo el cual el Prestamista entregará al Tomador, en calidad de préstamo, los Valores Negociables que se indican en el Anexo I a la presente Oferta de Préstamo, bajo el cual se establecen los términos y condiciones que regirán dicho contrato.\n\n"
            f"SEGUNDO: En caso que el Prestamista decida aceptar la presente Oferta de Préstamo, las obligaciones y derechos de las Partes serán estrictamente los que resultan del Anexo I adjunto a la presente.\n\n"
            f"TERCERO: La presente Oferta de Préstamo tiene vigencia por el plazo de 5 (cinco) días hábiles, considerándose aceptada si en o antes de dicho plazo, el Prestamista realiza la transferencia de los Valores Negociables a la cuenta comitente del Tomador, conforme se establece en la cláusula PRIMERA del Anexo I adjunto.\n\n"
            f"Atentamente,\n\n"
            f"____________________________\n"
            f"Por {sanitize_text(tomador)}\n"
            f"Aclaración:\n"
            f"Carácter:\n\n"
            f"ANEXO I\n"
            f"OFERTA DE PRÉSTAMO DE VALORES NEGOCIABLES\n"
            f"En el supuesto de ser aceptada la Oferta de Préstamo en los términos aquí previstos, de la cual la presente forma parte como Anexo I, se entenderá que se ha perfeccionado el siguiente contrato de préstamo (en adelante, el 'Contrato de Préstamo' o el 'Contrato' indistintamente), y tendrá como partes a:\n"
            f"a) {sanitize_text(prestamista)}, CUIT {sanitize_text(cuit_prestamista)}, con domicilio en {sanitize_text(domicilio_prestamista)} (en adelante, el 'Prestamista'), por una parte, y\n"
            f"b) {sanitize_text(tomador)}, CUIT {sanitize_text(cuit_tomador)}, con domicilio en {sanitize_text(domicilio_tomador)} (en adelante, el 'Tomador'), por la otra.\n\n"
            f"PRIMERA: El Prestamista transfiere al Tomador en calidad de préstamo, los siguientes valores negociables: {sanitize_text(especie)} por un valor nominal de {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}) con el alcance y extensión que se detalla en el Anexo II (en adelante, los 'Valores Negociables').\n\n"
            f"Los Valores Negociables se encuentran depositados en la cuenta comitente {sanitize_text(comitente_prestamista)}, de su titularidad, abierta en COHEN S.A (en adelante, la 'Cuenta del Prestamista').\n"
            f"El Tomador acepta recibir los Valores Negociables en su cuenta comitente N° {sanitize_text(comitente_tomador)} abierta en COHEN S.A. (en adelante, la 'Cuenta del Tomador'), obligándose a devolver los Valores Negociables mediante transferencia a la Cuenta del Prestamista y/u otra que éste indicare fehacientemente conforme previsión contemplada en la cláusula NOVENA del presente Anexo. La constancia de débito de dicha transferencia emitida por COHEN S.A. correspondiente a la Cuenta del Prestamista será suficiente recibo del Tomador por la recepción de los Valores Negociables.\n\n"
            f"SEGUNDA: El presente préstamo se establece por un plazo de {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses contados a partir de la transferencia de los Valores Negociables a la Cuenta del Tomador (en adelante, el 'Plazo'). Durante el Plazo, el Prestamista percibirá una tasa de interés equivalente al {sanitize_text(tasa_anual)}% nominal anual que será abonado, en pesos, por el Tomador al vencimiento del Plazo. El interés se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado.\n\n"
            f"El interés resultante será abonado en pesos desde la Cuenta del Tomador mediante transferencia a la cuenta bancaria de titularidad del Prestamista indicada en el Anexo II.\n")
    
    if moneda == "Dólares":
        body += (f"El mismo será calculado de acuerdo al Tipo de Cambio {sanitize_text(cuenta_bancaria)} del día de pago.\n\n")
    
    body += (f"TERCERA: La renovación de la vigencia del Contrato acaecerá de modo automático en ausencia de una notificación de cancelación anticipada conforme la cláusula CUARTA.\n\n"
            f"CUARTA: El Prestamista podrá solicitar la cancelación anticipada del préstamo de los Valores Negociables antes del vencimiento del Plazo, para lo cual deberá notificar por escrito al Tomador con una antelación de 48 horas hábiles a la efectiva fecha de cancelación. En caso de ejercerse tal derecho, el Tomador abonará en forma proporcional el importe de la contraprestación convenida en la cláusula SEGUNDA.\n\n"
            f"QUINTA: El Tomador se obliga a restituir los Valores Negociables al vencimiento del Plazo.\n\n"
            f"SEXTA: El Tomador se compromete a realizar todos aquellos actos necesarios para la conservación de los Valores Negociables, obligándose a restituirlos a la finalización del Plazo en igual cantidad y especie que los recibiera.\n\n"
            f"SÉPTIMA: El Tomador pagará todos los gastos que genere la operatoria objeto del presente Contrato.\n\n"
            f"OCTAVA: Todos los pagos que corresponda percibir por los Valores Negociables dados en préstamo corresponderán al Prestamista. En tal sentido, el Tomador deberá transferirlos a la Cuenta del Prestamista el día hábil posterior a su percepción.\n\n"
            f"NOVENA: La obligación de restituir los Valores Negociables no requiere interpelación judicial o extrajudicial alguna, configurándose su incumplimiento de pleno derecho por el solo incumplimiento material de la obligación de que se trate en la fecha estipulada, dando derecho al Prestamista a considerar vencido el Plazo y exigir la inmediata cancelación del Contrato de Préstamo y de los intereses devengados bajo el mismo.\n\n"
            f"DÉCIMA: El Prestamista asume el riesgo por las oscilaciones propias de los mercados que determinen variaciones de precios y/o cancelaciones de los Valores Negociables.\n\n"
            f"DÉCIMO PRIMERA: El tomador declara conocer que la falta de devolución de los Valores Negociables en tiempo y forma generará una penalidad del {sanitize_text(interes)}% mensual por cada día de retardo en el cumplimiento de su obligación de restituir.\n\n"
            f"DÉCIMO SEGUNDA: Estas operaciones no gozan del sistema de garantía de liquidación de Bolsas y Mercados Argentinos S.A. (BYMA).\n\n"
            f"DÉCIMO TERCERA: El Prestamista no asume ningún tipo de responsabilidad por las situaciones de mercado o incumplimiento por parte del emisor que se pudieran dar en relación a los Valores Negociables mientras se encuentren en poder del Tomador. Asimismo, el Prestamista no garantiza ningún tipo de beneficio económico como consecuencia de la utilización de los mismos.\n\n"
            f"DÉCIMO CUARTA: El Tomador no podrá ceder su posición contractual bajo el Contrato, ni ninguno de los derechos emergentes del mismo sin el consentimiento previo y escrito otorgado por el Prestamista.\n\n"
            f"DÉCIMO QUINTA: Toda modificación a este Contrato deberá ser realizada por las Partes por escrito y conforme las mismas formalidades que se observan en este Contrato.\n\n"
            f"DÉCIMO SEXTA: Para todos los efectos legales derivados de esta Oferta, las Partes constituyen sus domicilios en los indicados en el segundo párrafo del presente Anexo, donde se tendrán por válidas todas las notificaciones. Toda controversia relacionada al presente Contrato será resuelta en forma inapelable por el Tribunal de Arbitraje General de la Bolsa de Comercio de Buenos Aires por las reglas del arbitraje de derecho, que las partes declaran conocer y aceptar.\n\n"
            f"\nANEXO II\n"
            f"Condiciones de la operación de Préstamo de Títulos Valores:\n\n"
            f"Prestamista: {sanitize_text(prestamista)}, cuenta Comitente N° {sanitize_text(comitente_prestamista)} Depositante N° {sanitize_text(depositante_prestamista)}.\n\n"
            f"Tomador: {sanitize_text(tomador)}, cuenta comitente N° {sanitize_text(comitente_tomador)} Depositante N° {sanitize_text(depositante_tomador)}.\n\n"
            f"Especie: {sanitize_text(especie)} (código especie {sanitize_text(codigo_especie)}).\n\n"
            f"Valor Nominal: {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}).\n\n"
            f"Tasa: {sanitize_text(tasa_anual)}% nominal anual.\n\n"
            f"Interés: Se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado. Será abonado en pesos desde la Cuenta del Tomador mediante depósito en la Cuenta del Prestamista.\n")
    
    if moneda == "Dólares":
        body += (f" El mismo será calculado de acuerdo al Tipo de Cambio {sanitize_text(cuenta_bancaria)} del día de pago.\n")
    
    body += (f"Plazo: {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses.\n\n"
            f"Base de Cálculo: Actual/365.\n")

    pdf.chapter_body(body)
    return pdf.output(dest='S')

# Función para generar el PDF para PRESTAMO ENTRE CLIENTES T-BILLS
def generate_pdf_prestamo_entre_clientes_tbills(mes, dia, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuenta_bancaria, cuit_prestamista, domicilio_prestamista, cuit_tomador, domicilio_tomador):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    body = (f"Ciudad Autónoma de Buenos Aires, {sanitize_text(dia)} de {sanitize_text(mes)} de 2024\n\n"
            f"Sres.\n"
            f"{sanitize_text(prestamista)}\n"
            f"Presente\n\n"
            f"Ref.: Oferta de Préstamo\n\n"
            f"De nuestra mayor consideración:\n"
            f"Conforme a las conversaciones mantenidas, nos dirigimos a {sanitize_text(prestamista)} (en adelante, el 'Prestamista'), a fin de formular con carácter de irrevocable la presente Oferta de Préstamo de Valores Negociables (en adelante, la 'Oferta de Préstamo').\n"
            f"A los efectos de la presente Oferta de Préstamo, el Prestamista y {sanitize_text(tomador)} (en adelante, el 'Tomador') serán denominados en forma conjunta como las 'Partes'.\n\n"
            f"PRIMERO: El Tomador ofrece al Prestamista realizar un contrato de préstamo bajo el cual el Prestamista entregará al Tomador, en calidad de préstamo, los Valores Negociables que se indican en el Anexo I a la presente Oferta de Préstamo, bajo el cual se establecen los términos y condiciones que regirán dicho contrato.\n\n"
            f"SEGUNDO: En caso que el Prestamista decida aceptar la presente Oferta de Préstamo, las obligaciones y derechos de las Partes serán estrictamente los que resultan del Anexo I adjunto a la presente.\n\n"
            f"TERCERO: La presente Oferta de Préstamo tiene vigencia por el plazo de 5 (cinco) días hábiles, considerándose aceptada si en o antes de dicho plazo, el Prestamista realiza la transferencia de los Valores Negociables a la cuenta comitente del Tomador, conforme se establece en la cláusula PRIMERA del Anexo I adjunto.\n\n"
            f"Atentamente,\n\n"
            f"____________________________\n"
            f"Por {sanitize_text(tomador)}\n"
            f"Aclaración:\n"
            f"Carácter:\n\n"
            f"ANEXO I\n"
            f"OFERTA DE PRÉSTAMO DE VALORES NEGOCIABLES\n"
            f"En el supuesto de ser aceptada la Oferta de Préstamo en los términos aquí previstos, de la cual la presente forma parte como Anexo I, se entenderá que se ha perfeccionado el siguiente contrato de préstamo (en adelante, el 'Contrato de Préstamo' o el 'Contrato' indistintamente), y tendrá como partes a:\n"
            f"a) {sanitize_text(prestamista)}, CUIT {sanitize_text(cuit_prestamista)}, con domicilio en {sanitize_text(domicilio_prestamista)} (en adelante, el 'Prestamista'), por una parte, y\n"
            f"b) {sanitize_text(tomador)}, CUIT {sanitize_text(cuit_tomador)}, con domicilio en {sanitize_text(domicilio_tomador)} (en adelante, el 'Tomador'), por la otra.\n\n"
            f"PRIMERA: El Prestamista transfiere al Tomador en calidad de préstamo, los siguientes valores negociables: {sanitize_text(especie)} por un valor nominal de {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}) con el alcance y extensión que se detalla en el Anexo II (en adelante, los 'Valores Negociables').\n\n"
            f"Los Valores Negociables se encuentran depositados en la cuenta comitente {sanitize_text(comitente_prestamista)}, de su titularidad, abierta en Cohen S.A. (en adelante, la 'Cuenta del Prestamista').\n"
            f"El Tomador acepta recibir los Valores Negociables en su cuenta comitente N° {sanitize_text(comitente_tomador)} abierta en {sanitize_text(depositante_tomador)} (en adelante, la 'Cuenta del Tomador'), obligándose a devolver los Valores Negociables mediante transferencia a la Cuenta del Prestamista y/u otra que éste indicare fehacientemente conforme previsión contemplada en la cláusula NOVENA del presente Anexo. La constancia de débito de dicha transferencia emitida por COHEN S.A. correspondiente a la Cuenta del Prestamista será suficiente recibo del Tomador por la recepción de los Valores Negociables.\n\n"
            f"SEGUNDA: El presente préstamo se establece por un plazo de {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses contados a partir de la transferencia de los Valores Negociables a la Cuenta del Tomador (en adelante, el 'Plazo'). Durante el Plazo, el Prestamista percibirá una tasa de interés equivalente al {sanitize_text(tasa_anual)}% nominal anual que será abonado, en pesos, por el Tomador al vencimiento del Plazo. El interés se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado.\n\n"
            f"El interés resultante será abonado en pesos desde la Cuenta del Tomador mediante transferencia a la cuenta bancaria de titularidad del Prestamista indicada en el Anexo II. El mismo será calculado de acuerdo al Tipo de Cambio {sanitize_text(cuenta_bancaria)} del día de pago.\n"
            f"TERCERA: La renovación de la vigencia del Contrato acaecerá de modo automático en ausencia de una notificación de cancelación anticipada conforme la cláusula CUARTA.\n\n"
            f"CUARTA: El Prestamista podrá solicitar la cancelación anticipada del préstamo de los Valores Negociables antes del vencimiento del Plazo, para lo cual deberá notificar por escrito al Tomador con una antelación de 48 horas hábiles a la efectiva fecha de cancelación. En caso de ejercerse tal derecho, el Tomador abonará en forma proporcional el importe de la contraprestación convenida en la cláusula SEGUNDA.\n\n"
            f"QUINTA: El Tomador se obliga a restituir los Valores Negociables al vencimiento del Plazo.\n\n"
            f"SEXTA: El Tomador se compromete a realizar todos aquellos actos necesarios para la conservación de los Valores Negociables, obligándose a restituirlos a la finalización del Plazo en igual cantidad y especie que los recibiera.\n\n"
            f"SÉPTIMA: El Tomador pagará todos los gastos que genere la operatoria objeto del presente Contrato.\n\n"
            f"OCTAVA: La obligación de restituir los Valores Negociables no requiere interpelación judicial o extrajudicial alguna, configurándose su incumplimiento de pleno derecho por el solo incumplimiento material de la obligación de que se trate en la fecha estipulada, dando derecho al Prestamista a considerar vencido el Plazo y exigir la inmediata cancelación del Contrato de Préstamo y de los intereses devengados bajo el mismo.\n\n"
            f"NOVENA: El Prestamista asume el riesgo por las oscilaciones propias de los mercados que determinen variaciones de precios y/o cancelaciones de los Valores Negociables.\n\n"
            f"DÉCIMA: El tomador declara conocer que la falta de devolución de los Valores Negociables en tiempo y forma generará una penalidad del {sanitize_text(interes)}% mensual por cada día de retardo en el cumplimiento de su obligación de restituir.\n\n"
            f"DÉCIMO PRIMERA: Estas operaciones no gozan del sistema de garantía de liquidación de {sanitize_text(depositante_tomador)}.\n\n"
            f"DÉCIMO SEGUNDA: El Prestamista no asume ningún tipo de responsabilidad por las situaciones de mercado o incumplimiento por parte del emisor que se pudieran dar en relación a los Valores Negociables mientras se encuentren en poder del Tomador. Asimismo, el Prestamista no garantiza ningún tipo de beneficio económico como consecuencia de la utilización de los mismos.\n\n"
            f"DÉCIMO TERCERA: El Tomador no podrá ceder su posición contractual bajo el Contrato, ni ninguno de los derechos emergentes del mismo sin el consentimiento previo y escrito otorgado por el Prestamista.\n\n"
            f"DÉCIMO CUARTA: Toda modificación a este Contrato deberá ser realizada por las Partes por escrito y conforme las mismas formalidades que se observan en este Contrato.\n\n"
            f"DÉCIMO QUINTA: Para todos los efectos legales derivados de esta Oferta, las Partes constituyen sus domicilios en los indicados en el segundo párrafo del presente Anexo, donde se tendrán por válidas todas las notificaciones. Toda controversia relacionada al presente Contrato será resuelta en forma inapelable por el Tribunal de Arbitraje General de la {sanitize_text(depositante_tomador)} por las reglas del arbitraje de derecho, que las partes declaran conocer y aceptar.\n\n"
            f"\nANEXO II\n"
            f"Condiciones de la operación de Préstamo de Títulos Valores:\n\n"
            f"Prestamista: {sanitize_text(prestamista)}, cuenta Comitente N° {sanitize_text(comitente_prestamista)} Depositante N° {sanitize_text(depositante_prestamista)}.\n\n"
            f"Tomador: {sanitize_text(tomador)}, cuenta comitente N° {sanitize_text(comitente_tomador)} Depositante N° {sanitize_text(depositante_tomador)}.\n\n"
            f"Especie: {sanitize_text(especie)} (código especie {sanitize_text(codigo_especie)}).\n\n"
            f"Valor Nominal: {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}).\n\n"
            f"Tasa: {sanitize_text(tasa_anual)}% nominal anual.\n\n"
            f"Interés: Se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado. Será abonado en pesos desde la Cuenta del Tomador mediante depósito en la Cuenta del Prestamista. El mismo será calculado de acuerdo al Tipo de Cambio {sanitize_text(cuenta_bancaria)} del día de pago.\n\n"
            f"Plazo: {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses.\n\n"
            f"Base de Cálculo: Actual/365.\n")

    pdf.chapter_body(body)
    return pdf.output(dest='S')

def enviar_email(pdf_data, file_name):
    remitente = 'gallo@cohen.com.ar'
    destinatario = 'ddjj@cohen.com.ar'
    asunto = 'Carta Oferta Prestamo'
    cuerpo = 'Adjunto carta de prestamo.'

    # Configuración del servidor SMTP de Gmail
    servidor_smtp = 'smtp.gmail.com'
    puerto_smtp = 587
    usuario_smtp = 'gallo@cohen.com.ar'
    contrasena_smtp = 'Cambiar21!'

    try:
        # Creación del mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto
        mensaje.attach(MIMEText(cuerpo, 'plain', 'utf-8'))

        # Asegurarse de que pdf_data es del tipo bytes
        pdf_data = bytes(pdf_data) if isinstance(pdf_data, bytearray) else pdf_data

        # Adjuntar el archivo
        parte = MIMEBase('application', 'octet-stream')
        parte.set_payload(pdf_data)
        encoders.encode_base64(parte)
        parte.add_header('Content-Disposition', f"attachment; filename={file_name}")
        mensaje.attach(parte)

        # Conexión y envío del correo
        servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
        servidor.starttls()
        servidor.login(usuario_smtp, contrasena_smtp)
        texto = mensaje.as_string()
        servidor.sendmail(remitente, destinatario, texto)
        servidor.quit()
        st.success('Descarga el PDF del prestamo generado.')
    except Exception as e:
        st.error(f'Error al enviar el correo: {e}')
        
import streamlit as st

st.set_page_config(page_title="Generador de Oferta de Préstamo", layout="wide")

st.markdown("""
<style>
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        padding: 0.5rem;
        border: none;
        border-radius: 4px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #0052a3;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 4px;
        border: 1px solid #ccc;
    }
    h1 {
        color: #333;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("Generar archivo PDF para oferta de préstamos")

tipo_prestamo = st.selectbox("Tipo de préstamo", ["COHEN TOMADOR", "COHEN PRESTAMISTA", "COHEN TOMADOR T-BILLS", "COHEN PRESTAMISTA T-BILLS", "PRESTAMO ENTRE CLIENTES", "PRESTAMO ENTRE CLIENTES T-BILLS"])
dia = st.selectbox("Día", list(range(1, 32)))
mes = st.selectbox("Mes", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])
interes = st.selectbox("Tasa de Penalidad - Interés", [f"{i}%" for i in range(1, 21)])
prestamista = st.text_input("Prestamista")
comitente_prestamista = st.number_input("Número de comitente Prestamista", min_value=0, step=1)
depositante_prestamista = st.text_input("Depositante prestamista")
tomador = st.text_input("Tomador")
comitente_tomador = st.number_input("Número de comitente tomador", min_value=0, step=1)
depositante_tomador = st.text_input("Depositante tomador")
especie = st.text_input("Especie")
codigo_especie = st.text_input("Código Especie")

# Solo mostrar el campo "Moneda del instrumento" para los tipos de préstamos específicos
if tipo_prestamo in ["COHEN TOMADOR", "COHEN PRESTAMISTA", "PRESTAMO ENTRE CLIENTES"]:
    moneda = st.selectbox("Moneda del instrumento", ["Pesos", "Dólares"])

valor_nominal = st.number_input("Valor Nominal", min_value=0, step=1)
tasa_anual = st.selectbox("Tasa Anual", [f"{i}%" for i in range(1, 21)])
plazo = st.selectbox("Plazo (en meses)", list(range(1, 13)))

# Mostrar el campo "Tipo de cambio" si la moneda es "Dólares" o si es uno de los T-BILLS
if (tipo_prestamo in ["COHEN TOMADOR", "COHEN PRESTAMISTA", "PRESTAMO ENTRE CLIENTES"] and moneda == "Dólares") or tipo_prestamo in ["COHEN TOMADOR T-BILLS", "COHEN PRESTAMISTA T-BILLS", "PRESTAMO ENTRE CLIENTES T-BILLS"]:
    cuenta_bancaria = st.text_input("Tipo de cambio")

cuit = st.number_input("CUIT", min_value=0, step=1)
domicilio = st.text_input("Domicilio")

if tipo_prestamo in ["PRESTAMO ENTRE CLIENTES", "PRESTAMO ENTRE CLIENTES T-BILLS"]:
    st.markdown("### Información adicional para préstamos entre clientes")
    domicilio_prestamista = st.text_input("Domicilio Prestamista")
    cuit_prestamista = st.number_input("CUIT Prestamista", min_value=0, step=1)
    domicilio_tomador = st.text_input("Domicilio Tomador")
    cuit_tomador = st.number_input("CUIT Tomador", min_value=0, step=1)

if st.button("Generar PDF"):
    with st.spinner("Generando PDF..."):
        # Convertir los valores de los selectbox a formato adecuado
        interes = int(interes.replace('%', ''))
        tasa_anual = int(tasa_anual.replace('%', ''))
        
        try:
            # Siempre convertir valor_nominal y plazo a texto
            valor_nominal_texto = number_to_text(valor_nominal)
            plazo_texto = number_to_text(plazo)

            if tipo_prestamo == "COHEN TOMADOR":
                if moneda == "Pesos":
                    pdf_data = generate_pdf_cohen_tomador(mes, dia, moneda, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuit, domicilio)
                else:  # Para dólares
                    pdf_data = generate_pdf_cohen_tomador(mes, dia, moneda, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuit, domicilio, cuenta_bancaria)
            elif tipo_prestamo == "COHEN PRESTAMISTA":
                if moneda == "Pesos":
                    pdf_data = generate_pdf_cohen_prestamista(mes, dia, moneda, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuit, domicilio)
                else:  # Para dólares
                    pdf_data = generate_pdf_cohen_prestamista(mes, dia, moneda, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuit, domicilio, cuenta_bancaria)
            elif tipo_prestamo == "COHEN TOMADOR T-BILLS":
                pdf_data = generate_pdf_cohen_tomador_tbills(mes, dia, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuenta_bancaria, cuit, domicilio)
            elif tipo_prestamo == "COHEN PRESTAMISTA T-BILLS":
                pdf_data = generate_pdf_cohen_prestamista_tbills(mes, dia, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuenta_bancaria, cuit, domicilio)
            elif tipo_prestamo == "PRESTAMO ENTRE CLIENTES":
                if tipo_prestamo == "PRESTAMO ENTRE CLIENTES":
                    if moneda == "Pesos":
                        pdf_data = generate_pdf_prestamo_entre_clientes(mes, dia, moneda, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuit_prestamista, domicilio_prestamista, cuit_tomador, domicilio_tomador)
                    else:  # Para dólares
                        pdf_data = generate_pdf_prestamo_entre_clientes(mes, dia, moneda, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuit_prestamista, domicilio_prestamista, cuit_tomador, domicilio_tomador, cuenta_bancaria)
            elif tipo_prestamo == "PRESTAMO ENTRE CLIENTES T-BILLS":
                pdf_data = generate_pdf_prestamo_entre_clientes_tbills(mes, dia, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuenta_bancaria, cuit_prestamista, domicilio_prestamista, cuit_tomador, domicilio_tomador)
            
            # Convertir pdf_data a bytes si es un bytearray
            if isinstance(pdf_data, bytearray):
                pdf_data = bytes(pdf_data)
            
            # Enviar el correo automáticamente
            enviar_email(pdf_data, "oferta_prestamo.pdf")
            
            st.success("Recordá que el contrato debe ser firmado por las partes intervinientes!!!")
            st.download_button(label="Descargar PDF", data=pdf_data, file_name="oferta_prestamo.pdf", mime="application/pdf")
        
        except Exception as e:
            st.error(f"Error al generar el PDF: {str(e)}")
