from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def agregar_imagen(pdf, ruta_imagen, x, y, ancho, alto):
    pdf.drawInlineImage(ruta_imagen, x, y, width=ancho, height=alto)

def generar_pdf(nombre_archivo, x, y, z):
    pdf = canvas.Canvas(nombre_archivo, pagesize=letter)

    pdf.drawString(200, 750, "Datos de los sensores recolectados")

    ruta_imagen = "prueba.png"
    imagen1 = x
    imagen2 = y
    imagen3 = z
    

    alto = 200
    ancho = 400

    agregar_imagen(pdf, imagen1, 100, 500, 400, 200)
    agregar_imagen(pdf, imagen2, 100, 300, 400, 200)
    agregar_imagen(pdf, imagen3, 100, 100, 400, 200)

    pdf.save()

