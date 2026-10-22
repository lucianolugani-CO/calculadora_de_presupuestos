# pdf_presupuesto.py: arma el PDF. No calcula nada: recibe los numeros ya hechos.
from fpdf import FPDF

LOGO = "logo.png"


def renglon(pdf, texto, valor):
    # un renglon con el texto a la izquierda y el valor a la derecha
    pdf.cell(120, 9, texto)
    pdf.cell(0, 9, valor, align="R", new_x="LMARGIN", new_y="NEXT")


def armar_pdf(negocio, numero, fecha, cliente, nombres, cantidades, precios_unitarios,
              subtotal, descuento, iva, total):
    pdf = FPDF()                      # pdf es el documento
    pdf.add_page()

    # encabezado: logo + nombre + numero y fecha
    pdf.image(LOGO, x=10, y=10, w=28)
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, negocio, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Presupuesto N° {numero}", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Fecha: {fecha}", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)

    # cliente y renglones del pedido
    pdf.set_font("Helvetica", "", 12)
    renglon(pdf, "Cliente", cliente)
    pdf.ln(2)
    for i in range(len(nombres)):
        texto = f"{cantidades[i]} x {nombres[i]} (${precios_unitarios[i]:.2f} c/u)"
        renglon(pdf, texto, f"${cantidades[i] * precios_unitarios[i]:.2f}")
    pdf.ln(4)

    # resumen
    renglon(pdf, "Subtotal", f"${subtotal:.2f}")
    renglon(pdf, "Descuento", f"-${descuento:.2f}")
    renglon(pdf, "IVA 21%", f"${iva:.2f}")
    pdf.set_font("Helvetica", "B", 14)
    renglon(pdf, "TOTAL", f"${total:.2f}")

    # pie
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 6, "Presupuesto válido por 7 días.", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())
