import streamlit as st
from fpdf import FPDF

def generate_pdf(mes, dia, cliente, interes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, f"Ciudad Autónoma de Buenos Aires, {mes} de {dia} de 2024\n\n"
                         f"Sres.\n"
                         f"{cliente}\n"
                         f"Atención: [ ]\n"
                         f"Presente\n\n"
                         f"Ref.: Oferta de Préstamo\n\n"
                         f"De nuestra mayor consideración:\n"
                         f"Conforme a las conversaciones mantenidas, nos dirigimos a {cliente} (en adelante, el “Prestamista”), a fin de formular con carácter de irrevocable la presente Oferta de Préstamo de Valores Negociables (en adelante, la “Oferta de Préstamo”).\n"
                         f"A los efectos de la presente Oferta de Préstamo, el Prestamista y COHEN S.A. (en adelante, el “Tomador”) serán denominados en forma conjunta como las “Partes”.\n"
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
                         f"En el supuesto de ser aceptada la Oferta de Préstamo en los términos aquí previstos, de la cual la presente forma parte como Anexo I, se entenderá que se ha perfeccionado el siguiente contrato de préstamo (en adelante, el “Contrato de Préstamo” o el “Contrato” indistintamente), y tendrá como partes a:\n"
                         f"a) {cliente}, CUIT [CUIT], con domicilio en [DOMICILIO] (en adelante, el “Prestamista”), por una parte, y\n"
                         f"b) por la otra, COHEN S.A., CUIT 30-55854331-7, con domicilio en la calle Ortiz de Ocampo 3302, Módulo IV, piso 2° de la Ciudad Autónoma de Buenos Aires (en adelante, el “Tomador” y conjuntamente con el Prestamista, las “Partes”).\n\n"
                         f"PRIMERA: El Prestamista transfiere al Tomador en calidad de préstamo, los siguientes valores negociables: [ESPECIE] por un valor nominal de [VALORNOMINAL] con el alcance y extensión que se detalla en el Anexo II (en adelante, los “Valores Negociables”).\n"
                         f"Los Valores Negociables se encuentran depositados en la cuenta comitente [COMITENTEPRESTAMISTA], de su titularidad, abierta en COHEN S.A. (en adelante, la “Cuenta del Prestamista”).\n"
                         f"El Tomador acepta recibir los Valores Negociables en su cuenta comitente N° [COMITENTEPRESTAMISTA] abierta en COHEN S.A. (Agente de Negociación, Liquidación y Compensación Integral N° 21) (en adelante, la “Cuenta del Tomador”), obligándose a devolver los Valores Negociables mediante transferencia a la Cuenta del Prestamista y/u otra que éste indicare fehacientemente conforme previsión contemplada en la cláusula NOVENA del presente Anexo. La constancia de débito de dicha transferencia emitida por COHEN S.A. correspondiente a la Cuenta del Prestamista será suficiente recibo del Tomador por la recepción de los Valores Negociables.\n"
                         f"SEGUNDA: El presente préstamo se establece por un plazo de [PLAZO] meses contados a partir de la transferencia de los Valores Negociables a la Cuenta del Tomador (en adelante, el “Plazo”). Durante el Plazo, el Prestamista percibirá una tasa de interés equivalente al {interes}% nominal anual que será abonado, en pesos, por el Tomador al vencimiento del Plazo. El interés se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado.\n"
                         f"El interés resultante será abonado en pesos desde la Cuenta del Tomador mediante transferencia a la cuenta bancaria de titularidad del Prestamista indicada en el Anexo II. El mismo será calculado de acuerdo al Tipo de Cambio [ ] del día de pago.\n"
                         f"TERCERA: La renovación de la vigencia del Contrato acaecerá de modo automático en ausencia de una notificación de cancelación anticipada conforme la cláusula CUARTA.\n"
                         f"CUARTA: El Prestamista podrá solicitar la cancelación anticipada del préstamo de los Valores Negociables antes del vencimiento del Plazo, para lo cual deberá notificar por escrito al Tomador con una antelación de 48 horas hábiles a la efectiva fecha de cancelación. En caso de ejercerse tal derecho, el Tomador abonará en forma proporcional el importe de la contraprestación convenida en la cláusula SEGUNDA.\n"
                         f"QUINTA: El Tomador se obliga a restituir los Valores Negociables al vencimiento del Plazo.\n"
                         f"SEXTA: El Tomador se compromete a realizar todos aquellos actos necesarios para la conservación de los Valores Negociables, obligándose a restituirlos a la finalización del Plazo en igual cantidad y especie que los recibiera.\n"
                         f"SÉPTIMA: El Tomador pagará todos los gastos que genere la operatoria objeto del presente Contrato.\n"
                         f"OCTAVA: Todos los pagos que corresponda percibir por los Valores Negociables dados en préstamo corresponderán al Prestamista. En tal sentido, el Tomador deberá transferirlos a la Cuenta del Prestamista el día hábil posterior a su percepción.\n"
                         f"NOVENA: La obligación de restituir los Valores Negociables no requiere interpelación judicial o extrajudicial alguna, configurándose su incumplimiento de pleno derecho por el solo incumplimiento material de la obligación de que se trate en la fecha estipulada, dando derecho al Prestamista a considerar vencido el Plazo y exigir la inmediata cancelación del Contrato de Préstamo y de los intereses devengados bajo el mismo.\n"
                         f"DÉCIMA: El Prestamista asume el riesgo por las oscilaciones propias de los mercados que determinen variaciones de precios y/o cancelaciones de los Valores Negociables.\n"
                         f"DÉCIMO PRIMERA: El tomador declara conocer que la falta de devolución de los Valores Negociables en tiempo y forma generará una penalidad del {interes}% mensual por cada día de retardo en el cumplimiento de su obligación de restituir.\n"
                         f"DÉCIMO SEGUNDA: Estas operaciones no gozan del sistema de garantía de liquidación de Bolsas y Mercados Argentinos S.A. (BYMA).\n"
                         f"DÉCIMO TERCERA: El Prestamista no asume ningún tipo de responsabilidad por las situaciones de mercado o incumplimiento por parte del emisor que se pudieran dar en relación a los Valores Negociables mientras se encuentren en poder del Tomador. Asimismo, el Prestamista no garantiza ningún tipo de beneficio económico como consecuencia de la utilización de los mismos.\n"
                         f"DÉCIMO CUARTA: El Tomador no podrá ceder su posición contractual bajo el Contrato, ni ninguno de los derechos emergentes del mismo sin el consentimiento previo y escrito otorgado por el Prestamista.\n"
                         f"DÉCIMO QUINTA: Toda modificación a este Contrato deberá ser realizada por las Partes por escrito y conforme las mismas formalidades que se observan en este Contrato.\n"
                         f"DÉCIMO SEXTA: Para todos los efectos legales derivados de esta Oferta, las Partes constituyen sus domicilios en los indicados en el segundo párrafo del presente Anexo, donde se tendrán por válidas todas las notificaciones. Toda controversia relacionada al presente Contrato será resuelta en forma inapelable por el Tribunal de Arbitraje General de la Bolsa de Comercio de Buenos Aires por las reglas del arbitraje de derecho, que las partes declaran conocer y aceptar.\n"
                         f"\nANEXO II\n"
                         f"Condiciones de la operación de Préstamo de Títulos Valores:\n"
                         f"Prestamista: [PRESTAMISTA], cuenta Comitente N° [COMITENTEPRESTAMISTA] Depositante N° [DEPOSITANTEPRESTAMISTA].\n"
                         f"Tomador: [TOMADOR], cuenta comitente N° [COMITENTETOMADOR] Depositante N° [DEPOSITANTETOMADOR].\n"
                         f"Especie: [ESPECIE] (código especie [CODIGOESPECIE]).\n"
                         f"Valor Nominal: [VALORNOMINAL].\n"
                         f"Tasa: {interes}% nominal anual.\n"
                         f"Interés: Se calculará sobre el valor promedio de cierre de contado 48 horas de los Valores Negociables por el Plazo pactado. Será abonado en pesos desde la Cuenta del Tomador mediante depósito en la Cuenta del Prestamista. El mismo será calculado de acuerdo al Tipo de Cambio [ ] del día de pago.\n"
                         f"Plazo: [PLAZO] meses.\n"
                         f"Cuenta bancaria del Prestamista: [CUENTABANCARIA]\n"
                         f"Base de Cálculo: Actual/365.\n")

    return pdf.output(dest='S').encode('latin1')

# Interfaz de Streamlit
st.title("Generador de PDF de Oferta de Préstamo")

# Formulario de entrada
mes = st.text_input("Mes", "")
dia = st.text_input("Día", "")
cliente = st.text_input("Cliente", "")
interes = st.text_input("Interés", "")

# Botón para generar el PDF
if st.button("Generar PDF"):
    pdf_data = generate_pdf(mes, dia, cliente, interes)
    st.download_button(label="Descargar PDF", data=pdf_data, file_name="oferta_prestamo.pdf", mime="application/pdf")
