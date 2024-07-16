import streamlit as st
from fpdf import FPDF
import inflect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

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

# Función para convertir números en texto
def number_to_text(number):
    p = inflect.engine()
    return p.number_to_words(number, andword="").replace("-", " ").capitalize()

# Función para generar el PDF para COHEN TOMADOR
def generate_pdf_cohen_tomador(mes, dia, cliente, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, tasa_anual, plazo, cuenta_bancaria, cuit, domicilio):
    pdf = PDF()
    pdf.add_page()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    
    valor_nominal_texto = number_to_text(valor_nominal)
    plazo_texto = number_to_text(plazo)
    
    body = (f"Ciudad Autónoma de Buenos Aires, {sanitize_text(mes)} de {sanitize_text(dia)} de 2024\n\n"
            f"Sres.\n"
            f"{sanitize_text(cliente)}\n"
            f"Atención: [ ]\n"
            f"Presente\n\n"
            f"Ref.: Oferta de Préstamo\n\n"
            f"De nuestra mayor consideración:\n"
            f"Conforme a las conversaciones mantenidas, nos dirigimos a {sanitize_text(cliente)} (en adelante, el 'Prestamista'), a fin de formular con carácter de irrevocable la presente Oferta de Préstamo de Valores Negociables (en adelante, la 'Oferta de Préstamo').\n"
            f"A los efectos de la presente Oferta de Préstamo, el Prestamista y COHEN S.A. (en adelante, el 'Tomador') serán denominados en forma conjunta como las 'Partes'.\n"
            f"PRIMERO: El Tomador ofrece al Prestamista realizar un contrato de préstamo bajo el cual el Prestamista entregará al Tomador, en calidad de préstamo, los Valores Negociables que se indican en el Anexo I a la presente Oferta de Préstamo, bajo el cual se establecen los términos y condiciones que regirán dicho contrato.\n"
            f"SEGUNDO: En caso que el Prestamista decida aceptar la presente Oferta de Préstamo, las obligaciones y derechos de las Partes serán estrictamente los que resultan del Anexo I adjunto a la presente.\n"
            f"TERCERO: La presente Oferta de Préstamo tiene vigencia por el plazo de 5 (cinco) días hábiles, considerándose aceptada si en o antes de dicho plazo, el Prestamista realiza la transferencia de los Valores Negociables a la cuenta comitente del Tomador, conforme se establece en la cláusula PRIMERA del Anexo I adjunto.\n"
            f"Atentamente,\n\n"
            f"____________________________\n"
            f"Por COHEN S.A.\n"
            f"Aclaración:\n"
            f"Carácter:\n\n"
            f"____________________________\n"
            f"Por COHEN S.A.\n"
            f"Aclaración:\n"
            f"Carácter:\n\n"
            f"ANEXO I\n"
            f"OFERTA DE PRÉSTAMO DE VALORES NEGOCIABLES\n"
            f"En el supuesto de ser aceptada la Oferta de Préstamo en los términos aquí previstos, de la cual la presente forma parte como Anexo I, se entenderá que se ha perfeccionado el siguiente contrato de préstamo (en adelante, el 'Contrato de Préstamo' o el 'Contrato' indistintamente), y tendrá como partes a:\n"
            f"a) {sanitize_text(prestamista)}, CUIT {sanitize_text(cuit)}, con domicilio en {sanitize_text(domicilio)} (en adelante, el 'Prestamista'), por una parte, y\n"
            f"b) por la otra, COHEN S.A., CUIT 30-55854331-7, con domicilio en la calle Ortiz de Ocampo 3302, Módulo IV, piso 2° de la Ciudad Autónoma de Buenos Aires (en adelante, el 'Tomador' y conjuntamente con el Prestamista, las 'Partes').\n\n"
            f"PRIMERA: El Prestamista transfiere al Tomador en calidad de préstamo, los siguientes valores negociables: {sanitize_text(especie)} por un valor nominal de {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}) con el alcance y extensión que se detalla en el Anexo II (en adelante, los 'Valores Negociables').\n"
            f"Los Valores Negociables se encuentran depositados en la cuenta comitente {sanitize_text(comitente_prestamista)}, de su titularidad, abierta en COHEN S.A. (en adelante, la 'Cuenta del Prestamista').\n"
            f"El Tomador acepta recibir los Valores Negociables en su cuenta comitente N° {sanitize_text(comitente_tomador)} abierta en COHEN S.A. (Agente de Negociación, Liquidación y Compensación Integral N° 21) (en adelante, la 'Cuenta del Tomador'), obligándose a devolver los Valores Negociables mediante transferencia a la Cuenta del Prestamista y/u otra que éste indicare fehacientemente conforme previsión contemplada en la cláusula NOVENA del presente Anexo. La constancia de débito de dicha transferencia emitida por COHEN S.A. correspondiente a la Cuenta del Prestamista será suficiente recibo del Tomador por la recepción de los Valores Negociables.\n"
            f"SEGUNDA: El presente préstamo se establece por un plazo de {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses contados a partir de la transferencia de los Valores Negociables a la Cuenta del Tomador (en adelante, el 'Plazo'). Durante el Plazo, el Prestamista percibirá una tasa de interés equivalente al {sanitize_text(tasa_anual)}% nominal anual que será abonado, en pesos, por el Tomador al vencimiento del Plazo. El interés se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado.\n"
            f"El interés resultante será abonado en pesos desde la Cuenta del Tomador mediante transferencia a la cuenta bancaria de titularidad del Prestamista indicada en el Anexo II. El mismo será calculado de acuerdo al Tipo de Cambio [ ] del día de pago.\n"
            f"TERCERA: La renovación de la vigencia del Contrato acaecerá de modo automático en ausencia de una notificación de cancelación anticipada conforme la cláusula CUARTA.\n"
            f"CUARTA: El Prestamista podrá solicitar la cancelación anticipada del préstamo de los Valores Negociables antes del vencimiento del Plazo, para lo cual deberá notificar por escrito al Tomador con una antelación de 48 horas hábiles a la efectiva fecha de cancelación. En caso de ejercerse tal derecho, el Tomador abonará en forma proporcional el importe de la contraprestación convenida en la cláusula SEGUNDA.\n"
            f"QUINTA: El Tomador se obliga a restituir los Valores Negociables al vencimiento del Plazo.\n"
            f"SEXTA: El Tomador se compromete a realizar todos aquellos actos necesarios para la conservación de los Valores Negociables, obligándose a restituirlos a la finalización del Plazo en igual cantidad y especie que los recibiera.\n"
            f"SÉPTIMA: El Tomador pagará todos los gastos que genere la operatoria objeto del presente Contrato.\n"
            f"OCTAVA: Todos los pagos que corresponda percibir por los Valores Negociables dados en préstamo corresponderán al Prestamista. En tal sentido, el Tomador deberá transferirlos a la Cuenta del Prestamista el día hábil posterior a su percepción.\n"
            f"NOVENA: La obligación de restituir los Valores Negociables no requiere interpelación judicial o extrajudicial alguna, configurándose su incumplimiento de pleno derecho por el solo incumplimiento material de la obligación de que se trate en la fecha estipulada, dando derecho al Prestamista a considerar vencido el Plazo y exigir la inmediata cancelación del Contrato de Préstamo y de los intereses devengados bajo el mismo.\n"
            f"DÉCIMA: El Prestamista asume el riesgo por las oscilaciones propias de los mercados que determinen variaciones de precios y/o cancelaciones de los Valores Negociables.\n"
            f"DÉCIMO PRIMERA: El tomador declara conocer que la falta de devolución de los Valores Negociables en tiempo y forma generará una penalidad del {sanitize_text(interes)}% mensual por cada día de retardo en el cumplimiento de su obligación de restituir.\n"
            f"DÉCIMO SEGUNDA: Estas operaciones no gozan del sistema de garantía de liquidación de Bolsas y Mercados Argentinos S.A. (BYMA).\n"
            f"DÉCIMO TERCERA: El Prestamista no asume ningún tipo de responsabilidad por las situaciones de mercado o incumplimiento por parte del emisor que se pudieran dar en relación a los Valores Negociables mientras se encuentren en poder del Tomador. Asimismo, el Prestamista no garantiza ningún tipo de beneficio económico como consecuencia de la utilización de los mismos.\n"
            f"DÉCIMO CUARTA: El Tomador no podrá ceder su posición contractual bajo el Contrato, ni ninguno de los derechos emergentes del mismo sin el consentimiento previo y escrito otorgado por el Prestamista.\n"
            f"DÉCIMO QUINTA: Toda modificación a este Contrato deberá ser realizada por las Partes por escrito y conforme las mismas formalidades que se observan en este Contrato.\n"
            f"DÉCIMO SEXTA: Para todos los efectos legales derivados de esta Oferta, las Partes constituyen sus domicilios en los indicados en el segundo párrafo del presente Anexo, donde se tendrán por válidas todas las notificaciones. Toda controversia relacionada al presente Contrato será resuelta en forma inapelable por el Tribunal de Arbitraje General de la Bolsa de Comercio de Buenos Aires por las reglas del arbitraje de derecho, que las partes declaran conocer y aceptar.\n"
            f"\nANEXO II\n"
            f"Condiciones de la operación de Préstamo de Títulos Valores:\n"
            f"Prestamista: {sanitize_text(prestamista)}, cuenta Comitente N° {sanitize_text(comitente_prestamista)} Depositante N° {sanitize_text(depositante_prestamista)}.\n"
            f"Tomador: {sanitize_text(tomador)}, cuenta comitente N° {sanitize_text(comitente_tomador)} Depositante N° {sanitize_text(depositante_tomador)}.\n"
            f"Especie: {sanitize_text(especie)} (código especie {sanitize_text(codigo_especie)}).\n"
            f"Valor Nominal: {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}).\n"
            f"Tasa: {sanitize_text(tasa_anual)}% nominal anual.\n"
            f"Interés: Se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado. Será abonado en pesos desde la Cuenta del Tomador mediante depósito en la Cuenta del Prestamista. El mismo será calculado de acuerdo al Tipo de Cambio [ ] del día de pago.\n"
            f"Plazo: {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses.\n"
            f"Cuenta bancaria del Prestamista: {sanitize_text(cuenta_bancaria)}\n"
            f"Base de Cálculo: Actual/365.\n")

    pdf.chapter_body(body)
    return pdf.output(dest='S').encode('latin1')

# Función para generar el PDF para COHEN PRESTAMISTA
def generate_pdf_cohen_prestamista(mes, dia, cliente, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, tasa_anual, plazo, cuenta_bancaria, cuit, domicilio):
    pdf = PDF()
    pdf.add_page()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    
    valor_nominal_texto = number_to_text(valor_nominal)
    plazo_texto = number_to_text(plazo)
    
    body = (f"Ciudad Autónoma de Buenos Aires, {sanitize_text(dia)} de {sanitize_text(mes)} de 2024\n\n"
            f"Sres.\n"
            f"Cohen S.A.\n"
            f"Presente\n\n"
            f"Ref.: Oferta de Préstamo de Valores Negociables\n\n"
            f"De nuestra mayor consideración:\n"
            f"Conforme a las conversaciones mantenidas, nos dirigimos a Cohen S.A. (en adelante, el 'Prestamista'), a fin de formular con carácter de irrevocable la presente Oferta de Préstamo de Valores Negociables (en adelante, la 'Oferta de Préstamo').\n"
            f"A los efectos de la presente Oferta de Préstamo, el Prestamista y {sanitize_text(cliente)} (en adelante, el 'Tomador') serán denominados en forma conjunta como las 'Partes'.\n"
            f"PRIMERO: El Tomador ofrece al Prestamista realizar un contrato de préstamo bajo el cual el Prestamista entregará al Tomador, en calidad de préstamo, los Valores Negociables que se indican en el Anexo I a la presente Oferta de Préstamo, bajo el cual se establecen los términos y condiciones que regirán dicho contrato.\n"
            f"SEGUNDO: En caso que el Prestamista decida aceptar la presente Oferta de Préstamo, las obligaciones y derechos de las Partes serán estrictamente los que resultan del Anexo I adjunto a la presente.\n"
            f"TERCERO: La presente Oferta de Préstamo tiene vigencia por el plazo de 5 (cinco) días hábiles, considerándose aceptada si en o antes de dicho plazo, el Prestamista realiza la transferencia de los Valores Negociables a la cuenta comitente del Tomador, conforme se establece en la cláusula PRIMERA del Anexo I adjunto.\n"
            f"Atentamente,\n\n"
            f"____________________________\n"
            f"Por {sanitize_text(cliente)}\n"
            f"Aclaración:\n"
            f"Carácter:\n\n"
            f"ANEXO I\n"
            f"OFERTA DE PRÉSTAMO DE VALORES NEGOCIABLES\n"
            f"En el supuesto de ser aceptada la Oferta de Préstamo en los términos aquí previstos, de la cual la presente forma parte como Anexo I, se entenderá que se ha perfeccionado el siguiente contrato de préstamo (en adelante, el 'Contrato de Préstamo' o el 'Contrato' indistintamente), y tendrá como partes a:\n"
            f"a) {sanitize_text(cliente)}, CUIT {sanitize_text(cuit)}, con domicilio en {sanitize_text(domicilio)} (en adelante, el 'Tomador'), por una parte, y\n"
            f"b) por la otra, COHEN S.A., CUIT 30-55854331-7, con domicilio en la calle Ortiz de Ocampo 3302, Módulo IV, piso 2° de la Ciudad Autónoma de Buenos Aires (en adelante, el 'Prestamista' y conjuntamente con el Prestamista, las 'Partes').\n\n"
            f"PRIMERA: El Prestamista transfiere al Tomador en calidad de préstamo, los siguientes valores negociables: {sanitize_text(especie)} por un valor nominal de {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}) con el alcance y extensión que se detalla en el Anexo II (en adelante, los 'Valores Negociables').\n"
            f"Los Valores Negociables se encuentran depositados en la cuenta comitente {sanitize_text(comitente_prestamista)}, de su titularidad, abierta en COHEN S.A. (en adelante, la 'Cuenta del Prestamista').\n"
            f"El Tomador acepta recibir los Valores Negociables en su cuenta comitente N° {sanitize_text(comitente_tomador)} abierta en COHEN S.A. (Agente de Negociación, Liquidación y Compensación Integral N° 21) (en adelante, la 'Cuenta del Tomador'), obligándose a devolver los Valores Negociables mediante transferencia a la Cuenta del Prestamista y/u otra que éste indicare fehacientemente conforme previsión contemplada en la cláusula NOVENA del presente Anexo. La constancia de débito de dicha transferencia emitida por COHEN S.A. correspondiente a la Cuenta del Prestamista será suficiente recibo del Tomador por la recepción de los Valores Negociables.\n"
            f"SEGUNDA: El presente préstamo se establece por un plazo de {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses contados a partir de la transferencia de los Valores Negociables a la Cuenta del Tomador (en adelante, el 'Plazo'). Durante el Plazo, el Prestamista percibirá una tasa de interés equivalente al {sanitize_text(tasa_anual)}% nominal anual que será abonado, en pesos, por el Tomador al vencimiento del Plazo. El interés se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado.\n"
            f"El interés resultante será abonado en pesos desde la Cuenta del Tomador mediante transferencia a la cuenta bancaria de titularidad del Prestamista indicada en el Anexo II. El mismo será calculado de acuerdo al Tipo de Cambio [ ] del día de pago.\n"
            f"TERCERA: La renovación de la vigencia del Contrato acaecerá de modo automático en ausencia de una notificación de cancelación anticipada conforme la cláusula CUARTA.\n"
            f"CUARTA: El Prestamista podrá solicitar la cancelación anticipada del préstamo de los Valores Negociables antes del vencimiento del Plazo, para lo cual deberá notificar por escrito al Tomador con una antelación de 48 horas hábiles a la efectiva fecha de cancelación. En caso de ejercerse tal derecho, el Tomador abonará en forma proporcional el importe de la contraprestación convenida en la cláusula SEGUNDA.\n"
            f"QUINTA: El Tomador se obliga a restituir los Valores Negociables al vencimiento del Plazo.\n"
            f"SEXTA: El Tomador se compromete a realizar todos aquellos actos necesarios para la conservación de los Valores Negociables, obligándose a restituirlos a la finalización del Plazo en igual cantidad y especie que los recibiera.\n"
            f"SÉPTIMA: El Tomador pagará todos los gastos que genere la operatoria objeto del presente Contrato.\n"
            f"OCTAVA: Todos los pagos que corresponda percibir por los Valores Negociables dados en préstamo corresponderán al Prestamista. En tal sentido, el Tomador deberá transferirlos a la Cuenta del Prestamista el día hábil posterior a su percepción.\n"
            f"NOVENA: La obligación de restituir los Valores Negociables no requiere interpelación judicial o extrajudicial alguna, configurándose su incumplimiento de pleno derecho por el solo incumplimiento material de la obligación de que se trate en la fecha estipulada, dando derecho al Prestamista a considerar vencido el Plazo y exigir la inmediata cancelación del Contrato de Préstamo y de los intereses devengados bajo el mismo.\n"
            f"DÉCIMA: El tomador declara conocer que la falta de devolución de los Valores Negociables en tiempo y forma generará una penalidad del {sanitize_text(interes)}% mensual por cada día de retardo en el cumplimiento de su obligación de restituir.\n"
            f"DÉCIMO PRIMERA: Estas operaciones no gozan del sistema de garantía de liquidación de Bolsas y Mercados Argentinos S.A. (BYMA).\n"
            f"DÉCIMO SEGUNDA: El Prestamista no asume ningún tipo de responsabilidad por las situaciones de mercado o incumplimiento por parte del emisor que se pudieran dar en relación a los Valores Negociables mientras se encuentren en poder del Tomador. Asimismo, el Prestamista no garantiza ningún tipo de beneficio económico como consecuencia de la utilización de los mismos.\n"
            f"DÉCIMO TERCERA: El Tomador no podrá ceder su posición contractual bajo el Contrato, ni ninguno de los derechos emergentes del mismo sin el consentimiento previo y escrito otorgado por el Prestamista.\n"
            f"DÉCIMO CUARTA: Toda modificación a este Contrato deberá ser realizada por las Partes por escrito y conforme las mismas formalidades que se observan en este Contrato.\n"
            f"DÉCIMO QUINTA: Para todos los efectos legales derivados de esta Oferta, las Partes constituyen sus domicilios en los indicados en el segundo párrafo del presente Anexo, donde se tendrán por válidas todas las notificaciones. Toda controversia relacionada al presente Contrato será resuelta en forma inapelable por el Tribunal de Arbitraje General de la Bolsa de Comercio de Buenos Aires por las reglas del arbitraje de derecho, que las partes declaran conocer y aceptar.\n"
            f"\nANEXO II\n"
            f"Condiciones de la operación de Préstamo de Títulos Valores:\n"
            f"Prestamista: {sanitize_text(prestamista)}, cuenta Comitente N° {sanitize_text(comitente_prestamista)} Depositante N° {sanitize_text(depositante_prestamista)}.\n"
            f"Tomador: {sanitize_text(tomador)}, cuenta comitente N° {sanitize_text(comitente_tomador)} Depositante N° {sanitize_text(depositante_tomador)}.\n"
            f"Especie: {sanitize_text(especie)} (código especie {sanitize_text(codigo_especie)}).\n"
            f"Valor Nominal: {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}).\n"
            f"Tasa: {sanitize_text(tasa_anual)}% nominal anual.\n"
            f"Interés: Se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado. Será abonado en pesos desde la Cuenta del Tomador mediante depósito en la Cuenta del Prestamista. El mismo será calculado de acuerdo al Tipo de Cambio [ ] del día de pago.\n"
            f"Plazo: {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses.\n"
            f"Cuenta bancaria del Prestamista: {sanitize_text(cuenta_bancaria)}\n"
            f"Base de Cálculo: Actual/365.\n")

    pdf.chapter_body(body)
    return pdf.output(dest='S').encode('latin1')

# Función para generar el PDF para COHEN TOMADOR T-BILLS
def generate_pdf_cohen_tomador_tbills(mes, dia, cliente, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuenta_bancaria, cuit, domicilio):
    pdf = PDF()
    pdf.add_page()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    
    body = (f"Ciudad Autónoma de Buenos Aires, {sanitize_text(dia)} de {sanitize_text(mes)} de 2024\n\n"
            f"Sres.\n"
            f"{sanitize_text(cliente)}\n"
            f"Atención: [ ]\n"
            f"Presente\n\n"
            f"Ref.: Oferta de Préstamo\n\n"
            f"De nuestra mayor consideración:\n"
            f"Conforme a las conversaciones mantenidas, nos dirigimos a {sanitize_text(cliente)} (en adelante, el 'Prestamista'), a fin de formular con carácter de irrevocable la presente Oferta de Préstamo de Valores Negociables (en adelante, la 'Oferta de Préstamo').\n"
            f"A los efectos de la presente Oferta de Préstamo, el Prestamista y COHEN S.A. (en adelante, el 'Tomador') serán denominados en forma conjunta como las 'Partes'.\n"
            f"PRIMERO: El Tomador ofrece al Prestamista realizar un contrato de préstamo bajo el cual el Prestamista entregará al Tomador, en calidad de préstamo, los Valores Negociables que se indican en el Anexo I a la presente Oferta de Préstamo, bajo el cual se establecen los términos y condiciones que regirán dicho contrato.\n"
            f"SEGUNDO: En caso que el Prestamista decida aceptar la presente Oferta de Préstamo, las obligaciones y derechos de las Partes serán estrictamente los que resultan del Anexo I adjunto a la presente.\n"
            f"TERCERO: La presente Oferta de Préstamo tiene vigencia por el plazo de 5 (cinco) días hábiles, considerándose aceptada si en o antes de dicho plazo, el Prestamista realiza la transferencia de los Valores Negociables a la cuenta comitente del Tomador, conforme se establece en la cláusula PRIMERA del Anexo I adjunto.\n"
            f"Atentamente,\n\n"
            f"____________________________\n"
            f"Por COHEN S.A.\n"
            f"Aclaración:\n"
            f"Carácter:\n\n"
            f"____________________________\n"
            f"Por COHEN S.A.\n"
            f"Aclaración:\n"
            f"Carácter:\n\n"
            f"ANEXO I\n"
            f"OFERTA DE PRÉSTAMO DE VALORES NEGOCIABLES\n"
            f"En el supuesto de ser aceptada la Oferta de Préstamo en los términos aquí previstos, de la cual la presente forma parte como Anexo I, se entenderá que se ha perfeccionado el siguiente contrato de préstamo (en adelante, el 'Contrato de Préstamo' o el 'Contrato' indistintamente), y tendrá como partes a:\n"
            f"a) {sanitize_text(cliente)}, CUIT {sanitize_text(cuit)}, con domicilio en {sanitize_text(domicilio)} (en adelante, el 'Prestamista'), por una parte, y\n"
            f"b) por la otra, COHEN S.A., CUIT 30-55854331-7, con domicilio en la calle Ortiz de Ocampo 3302, Módulo IV, piso 2° de la Ciudad Autónoma de Buenos Aires (en adelante, el 'Tomador' y conjuntamente con el Prestamista, las 'Partes').\n\n"
            f"PRIMERA: El Prestamista transfiere al Tomador en calidad de préstamo, los siguientes valores negociables: {sanitize_text(especie)} por un valor nominal de {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}) con el alcance y extensión que se detalla en el Anexo II (en adelante, los 'Valores Negociables').\n"
            f"Los Valores Negociables se encuentran depositados en la cuenta comitente {sanitize_text(comitente_prestamista)}, de su titularidad, abierta en COHEN S.A. (en adelante, la 'Cuenta del Prestamista').\n"
            f"El Tomador acepta recibir los Valores Negociables en su cuenta comitente N° {sanitize_text(comitente_tomador)} abierta en COHEN S.A. (Agente de Negociación, Liquidación y Compensación Integral N° 21) (en adelante, la 'Cuenta del Tomador'), obligándose a devolver los Valores Negociables mediante transferencia a la Cuenta del Prestamista y/u otra que éste indicare fehacientemente conforme previsión contemplada en la cláusula NOVENA del presente Anexo. La constancia de débito de dicha transferencia emitida por COHEN S.A. correspondiente a la Cuenta del Prestamista será suficiente recibo del Tomador por la recepción de los Valores Negociables.\n"
            f"SEGUNDA: El presente préstamo se establece por un plazo de {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) mes contados a partir de la transferencia de los Valores Negociables a la Cuenta del Tomador (en adelante, el 'Plazo'). Durante el Plazo, el Prestamista percibirá una tasa de interés equivalente al {sanitize_text(tasa_anual)}% nominal anual que será abonado, en pesos, por el Tomador al vencimiento del Plazo. El interés se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado.\n"
            f"El interés resultante será abonado en pesos desde la Cuenta del Tomador mediante transferencia a la cuenta bancaria de titularidad del Prestamista indicada en el Anexo II. El mismo será calculado de acuerdo al Tipo de Cambio [ ] del día de pago.\n"
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
            f"\nANEXO II\n"
            f"Condiciones de la operación de Préstamo de Títulos Valores:\n"
            f"Prestamista: {sanitize_text(prestamista)}, cuenta Comitente N° {sanitize_text(comitente_prestamista)} Depositante N° {sanitize_text(depositante_prestamista)}.\n"
            f"Tomador: {sanitize_text(tomador)}, cuenta comitente N° {sanitize_text(comitente_tomador)} Depositante N° {sanitize_text(depositante_tomador)}.\n"
            f"Especie: {sanitize_text(especie)} (código especie {sanitize_text(codigo_especie)}).\n"
            f"Valor Nominal: {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}).\n"
            f"Tasa: {sanitize_text(tasa_anual)}% nominal anual.\n"
            f"Interés: Se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado. Será abonado en pesos desde la Cuenta del Tomador mediante depósito en la Cuenta del Prestamista. El mismo será calculado de acuerdo al Tipo de Cambio [ ] del día de pago.\n"
            f"Plazo: {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses.\n"
            f"Cuenta bancaria del Prestamista: {sanitize_text(cuenta_bancaria)}\n"
            f"Base de Cálculo: Actual/365.\n")

    pdf.chapter_body(body)
    return pdf.output(dest='S').encode('latin1')

# Función para generar el PDF para COHEN PRESTAMISTA T-BILLS
def generate_pdf_cohen_prestamista_tbills(mes, dia, cliente, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuenta_bancaria, cuit, domicilio):
    pdf = PDF()
    pdf.add_page()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    
    body = (f"Ciudad Autónoma de Buenos Aires, {sanitize_text(dia)} de {sanitize_text(mes)} de 2024\n\n"
            f"Sres.\n"
            f"Cohen S.A.\n"
            f"Presente\n\n"
            f"Ref.: Oferta de Préstamo de Valores Negociables\n\n"
            f"De nuestra mayor consideración:\n"
            f"Conforme a las conversaciones mantenidas, nos dirigimos a Cohen S.A. (en adelante, el 'Prestamista'), a fin de formular con carácter de irrevocable la presente Oferta de Préstamo de Valores Negociables (en adelante, la 'Oferta de Préstamo').\n"
            f"A los efectos de la presente Oferta de Préstamo, el Prestamista y {sanitize_text(cliente)} (en adelante, el 'Tomador') serán denominados en forma conjunta como las 'Partes'.\n"
            f"PRIMERO: El Tomador ofrece al Prestamista realizar un contrato de préstamo bajo el cual el Prestamista entregará al Tomador, en calidad de préstamo, los Valores Negociables que se indican en el Anexo I a la presente Oferta de Préstamo, bajo el cual se establecen los términos y condiciones que regirán dicho contrato.\n"
            f"SEGUNDO: En caso que el Prestamista decida aceptar la presente Oferta de Préstamo, las obligaciones y derechos de las Partes serán estrictamente los que resultan del Anexo I adjunto a la presente.\n"
            f"TERCERO: La presente Oferta de Préstamo tiene vigencia por el plazo de 5 (cinco) días hábiles, el Prestamista realiza la transferencia de los Valores Negociables a la cuenta comitente del Tomador, conforme se establece en la cláusula PRIMERA del Anexo I adjunto.\n"
            f"Atentamente,\n\n"
            f"____________________________\n"
            f"Por {sanitize_text(cliente)}\n"
            f"Aclaración:\n"
            f"Carácter:\n\n"
            f"ANEXO I\n"
            f"OFERTA DE PRÉSTAMO DE VALORES NEGOCIABLES\n"
            f"En el supuesto de ser aceptada la Oferta de Préstamo en los términos aquí previstos, de la cual la presente forma parte como Anexo I, se entenderá que se ha perfeccionado el siguiente contrato de préstamo (en adelante, el 'Contrato de Préstamo' o el 'Contrato' indistintamente), y tendrá como partes a:\n"
            f"a) {sanitize_text(cliente)}, CUIT {sanitize_text(cuit)}, con domicilio en {sanitize_text(domicilio)} (en adelante, el 'Tomador'), por una parte, y\n"
            f"b) por la otra, COHEN S.A., CUIT 30-55854331-7, con domicilio en la calle Ortiz de Ocampo 3302, Módulo IV, piso 2° de la Ciudad Autónoma de Buenos Aires (en adelante, el 'Prestamista' y conjuntamente con el Prestamista, las 'Partes').\n\n"
            f"PRIMERA: El Prestamista transfiere al Tomador en calidad de préstamo, los siguientes valores negociables: {sanitize_text(especie)} por un valor nominal de {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}) con el alcance y extensión que se detalla en el Anexo II (en adelante, los 'Valores Negociables').\n"
            f"Los Valores Negociables se encuentran depositados en la cuenta comitente {sanitize_text(comitente_prestamista)}, de su titularidad, abierta en COHEN S.A. (en adelante, la 'Cuenta del Prestamista').\n"
            f"El Tomador acepta recibir los Valores Negociables en su cuenta comitente N° {sanitize_text(comitente_tomador)} abierta en COHEN S.A. (Agente de Negociación, Liquidación y Compensación Integral N° 21) (en adelante, la 'Cuenta del Tomador'), obligándose a devolver los Valores Negociables mediante transferencia a la Cuenta del Prestamista y/u otra que éste indicare fehacientemente conforme previsión contemplada en la cláusula NOVENA del presente Anexo. La constancia de débito de dicha transferencia emitida por COHEN S.A. correspondiente a la Cuenta del Prestamista será suficiente recibo del Tomador por la recepción de los Valores Negociables.\n"
            f"SEGUNDA: El presente préstamo se establece por un plazo de {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses contados a partir de la transferencia de los Valores Negociables a la Cuenta del Tomador (en adelante, el 'Plazo'). Durante el Plazo, el Prestamista percibirá una tasa de interés equivalente al {sanitize_text(tasa_anual)}% nominal anual que será abonado, en pesos, por el Tomador al vencimiento del Plazo. El interés se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado.\n"
            f"El interés resultante será abonado en pesos desde la Cuenta del Tomador mediante transferencia a la cuenta bancaria de titularidad del Prestamista indicada en el Anexo II. El mismo será calculado de acuerdo al Tipo de Cambio [ ] del día de pago.\n"
            f"TERCERA: La renovación de la vigencia del Contrato acaecerá de modo automático en ausencia de una notificación de cancelación anticipada conforme la cláusula CUARTA.\n"
            f"CUARTA: El Prestamista podrá solicitar la cancelación anticipada del préstamo de los Valores Negociables antes del vencimiento del Plazo, para lo cual deberá notificar por escrito al Tomador con una antelación de 48 horas hábiles a la efectiva fecha de cancelación. En caso de ejercerse tal derecho, el Tomador abonará en forma proporcional el importe de la contraprestación convenida en la cláusula SEGUNDA.\n"
            f"QUINTA: El Tomador se obliga a restituir los Valores Negociables al vencimiento del Plazo.\n"
            f"SEXTA: El Tomador se compromete a realizar todos aquellos actos necesarios para la conservación de los Valores Negociables, obligándose a restituirlos a la finalización del Plazo en igual cantidad a la que los recibiera.\n"
            f"SÉPTIMA: El Tomador pagará todos los gastos que genere la operatoria objeto del presente Contrato.\n"
            f"OCTAVA: La obligación de restituir los Valores Negociables no requiere interpelación judicial o extrajudicial alguna, configurándose su incumplimiento de pleno derecho por el solo incumplimiento material de la obligación de que se trate en la fecha estipulada, dando derecho al Prestamista a considerar vencido el Plazo y exigir la inmediata cancelación del Contrato de Préstamo y de los intereses devengados bajo el mismo.\n"
            f"NOVENA: El tomador declara conocer que la falta de devolución de los Valores Negociables en tiempo y forma generará una penalidad del {sanitize_text(interes)}% mensual por cada día de retardo en el cumplimiento de su obligación de restituir.\n"
            f"DÉCIMA: Estas operaciones no gozan del sistema de garantía de liquidación de Bolsas y Mercados Argentinos S.A. (BYMA).\n"
            f"DÉCIMO PRIMERA: El Prestamista no asume ningún tipo de responsabilidad por las situaciones de mercado o incumplimiento por parte del emisor que se pudieran dar en relación a los Valores Negociables mientras se encuentren en poder del Tomador. Asimismo, el Prestamista no garantiza ningún tipo de beneficio económico como consecuencia de la utilización de los mismos.\n"
            f"DÉCIMO SEGUNDA: El Tomador no podrá ceder su posición contractual bajo el Contrato, ni ninguno de los derechos emergentes del mismo sin el consentimiento previo y escrito otorgado por el Prestamista.\n"
            f"DÉCIMO TERCERA: Toda modificación a este Contrato deberá ser realizada por las Partes por escrito y conforme las mismas formalidades que se observan en este Contrato.\n"
            f"DÉCIMO CUARTA: Para todos los efectos legales derivados de esta Oferta, las Partes constituyen sus domicilios en los indicados en el segundo párrafo del presente Anexo, donde se tendrán por válidas todas las notificaciones. Toda controversia relacionada al presente Contrato será resuelta en forma inapelable por el Tribunal de Arbitraje General de la Bolsa de Comercio de Buenos Aires por las reglas del arbitraje de derecho, que las partes declaran conocer y aceptar.\n"
            f"\nANEXO II\n"
            f"Condiciones de la operación de Préstamo de Títulos Valores:\n"
            f"Prestamista: {sanitize_text(prestamista)}, cuenta Comitente N° {sanitize_text(comitente_prestamista)} Depositante N° {sanitize_text(depositante_prestamista)}.\n"
            f"Tomador: {sanitize_text(tomador)}, cuenta comitente N° {sanitize_text(comitente_tomador)} Depositante N° {sanitize_text(depositante_tomador)}.\n"
            f"Especie: {sanitize_text(especie)} (código especie {sanitize_text(codigo_especie)}).\n"
            f"Valor Nominal: {sanitize_text(valor_nominal)} ({sanitize_text(valor_nominal_texto)}).\n"
            f"Tasa: {sanitize_text(tasa_anual)}% nominal anual.\n"
            f"Interés: Se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado. Será abonado en pesos desde la Cuenta del Tomador mediante depósito en la Cuenta del Prestamista. El mismo será calculado de acuerdo al Tipo de Cambio [ ] del día de pago.\n"
            f"Plazo: {sanitize_text(plazo)} ({sanitize_text(plazo_texto)}) meses.\n"
            f"Cuenta bancaria del Prestamista: {sanitize_text(cuenta_bancaria)}\n"
            f"Base de Cálculo: Actual/365.\n")

    pdf.chapter_body(body)
    return pdf.output(dest='S').encode('latin1')

def enviar_email(pdf_data, file_name):
    remitente = 'tu_correo@gmail.com'
    destinatario = 'ddjj@cohen.com.ar'
    asunto = 'Archivo generado'
    cuerpo = 'Adjunto el archivo generado.'

    # Configuración del servidor SMTP de Gmail
    servidor_smtp = 'smtp.gmail.com'
    puerto_smtp = 587
    usuario_smtp = 'tu_correo@gmail.com'
    contrasena_smtp = 'tu_contraseña_de_gmail'

    # Creación del mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Adjuntar el archivo
    parte = MIMEBase('application', 'octet-stream')
    parte.set_payload(pdf_data)
    encoders.encode_base64(parte)
    parte.add_header('Content-Disposition', f"attachment; filename= {file_name}")
    mensaje.attach(parte)

    # Conexión y envío del correo
    servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
    servidor.starttls()
    servidor.login(usuario_smtp, contrasena_smtp)
    texto = mensaje.as_string()
    servidor.sendmail(remitente, destinatario, texto)
    servidor.quit()
    print('Correo enviado exitosamente')

# Interfaz de Streamlit
st.title("Generador de PDF de Oferta de Préstamo")

# Selección del tipo de préstamo
tipo_prestamo = st.selectbox("Seleccione el tipo de préstamo", ["COHEN TOMADOR", "COHEN PRESTAMISTA", "COHEN TOMADOR T-BILLS", "COHEN PRESTAMISTA T-BILLS"])

# Campos para seleccionar el mes y el día
mes = st.selectbox("Mes", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])
dia = st.selectbox("Día", list(range(1, 32)))

# Otros campos necesarios
cliente = st.text_input("Cliente", "")
interes = st.text_input("Interés", "")
prestamista = st.text_input("Prestamista", "")
comitente_prestamista = st.text_input("Comitente Prestamista", "")
depositante_prestamista = st.text_input("Depositante Prestamista", "")
tomador = st.text_input("Tomador", "")
comitente_tomador = st.text_input("Comitente Tomador", "")
depositante_tomador = st.text_input("Depositante Tomador", "")
especie = st.text_input("Especie", "")
codigo_especie = st.text_input("Código Especie", "")
valor_nominal = st.text_input("Valor Nominal", "")
tasa_anual = st.text_input("Tasa Anual", "")
plazo = st.text_input("Plazo (en meses)", "")
cuenta_bancaria = st.text_input("Cuenta Bancaria del Prestamista", "")
cuit = st.text_input("CUIT", "")
domicilio = st.text_input("Domicilio", "")

# Botón para generar el PDF
if st.button("Generar PDF"):
    if tipo_prestamo == "COHEN TOMADOR":
        pdf_data = generate_pdf_cohen_tomador(mes, dia, cliente, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, tasa_anual, plazo, cuenta_bancaria, cuit, domicilio)
    elif tipo_prestamo == "COHEN PRESTAMISTA":
        pdf_data = generate_pdf_cohen_prestamista(mes, dia, cliente, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, tasa_anual, plazo, cuenta_bancaria, cuit, domicilio)
    elif tipo_prestamo == "COHEN TOMADOR T-BILLS":
        valor_nominal_texto = number_to_text(valor_nominal)
        plazo_texto = number_to_text(plazo)
        pdf_data = generate_pdf_cohen_tomador_tbills(mes, dia, cliente, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuenta_bancaria, cuit, domicilio)
    elif tipo_prestamo == "COHEN PRESTAMISTA T-BILLS":
        valor_nominal_texto = number_to_text(valor_nominal)
        plazo_texto = number_to_text(plazo)
        pdf_data = generate_pdf_cohen_prestamista_tbills(mes, dia, cliente, interes, prestamista, comitente_prestamista, depositante_prestamista, tomador, comitente_tomador, depositante_tomador, especie, codigo_especie, valor_nominal, valor_nominal_texto, tasa_anual, plazo, plazo_texto, cuenta_bancaria, cuit, domicilio)
    
    st.download_button(label="Descargar PDF", data=pdf_data, file_name="oferta_prestamo.pdf", mime="application/pdf")
    
    # Enviar el PDF por correo electrónico
    enviar_email(pdf_data, "oferta_prestamo.pdf")
