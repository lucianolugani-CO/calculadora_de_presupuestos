import streamlit as st
import mi_negocio
import calculos
import pdf_presupuesto

RENGLONES = 3


st.title(mi_negocio.NOMBRE_NEGOCIO)
st.caption(mi_negocio.RUBRO)
numero = st.number_input("N° de presupuesto", min_value=1, step=1)
fecha = st.date_input("Fecha")
cliente = st.text_input("Nombre del cliente")

# los renglones del pedido: solo se guardan los que tienen cantidad
nombres = []
cantidades = []
precios_unitarios = []
for i in range(RENGLONES):
    producto = st.selectbox(f"Producto {i + 1}", mi_negocio.productos)
    cantidad = st.number_input(f"Cantidad {i + 1}", min_value=0, step=1)
    if cantidad > 0:
        pos = calculos.buscar_posicion(mi_negocio.productos, producto)
        nombres.append(producto)
        cantidades.append(cantidad)
        precios_unitarios.append(mi_negocio.precios[pos])

pago = st.radio("Forma de pago", [calculos.EFECTIVO, calculos.TRANSFERENCIA])

subtotal = calculos.calcular_subtotal(cantidades, precios_unitarios)
con_descuento = calculos.aplicar_descuento(subtotal, pago)
descuento = round(subtotal - con_descuento, 2)
iva = calculos.calcular_iva(con_descuento)
total = round(con_descuento + iva, 2)

st.divider()
st.write(f"Subtotal: {subtotal} pesos")
st.write(f"Descuento: {descuento} pesos")
st.write(f"IVA 21%: {iva} pesos")
st.metric("TOTAL", f"${total}")

if len(nombres) == 0:
    st.warning("Cargá al menos un producto para generar el presupuesto.")
else:
    archivo = pdf_presupuesto.armar_pdf(
        negocio=mi_negocio.NOMBRE_NEGOCIO, numero=numero, fecha=fecha,
        cliente=cliente, nombres=nombres, cantidades=cantidades,
        precios_unitarios=precios_unitarios, subtotal=subtotal,
        descuento=descuento, iva=iva, total=total)
    st.download_button("Descargar presupuesto (PDF)", archivo,
                       file_name=f"presupuesto_{numero}.pdf", mime="application/pdf")
