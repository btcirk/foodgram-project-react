import io

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def pdf_generate(cart):
    buffer = io.BytesIO()
    pdfmetrics.registerFont(TTFont("OpenSans", "OpenSans-Regular.ttf", "UTF-8"))
    p = canvas.Canvas(buffer)
    p.setFont("OpenSans", size=24)
    p.drawString(200, 800, "Список ингредиентов")
    p.setFont("OpenSans", size=16)
    height = 750
    for item in cart:
        p.drawString(75, height, f'- {item} ({cart[item]["measurement_unit"]}) - {cart[item]["amount"]}')
        height -= 25
    p.showPage()
    p.save()
    return buffer
