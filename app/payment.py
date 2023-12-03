from flask import (Blueprint, render_template, request,
                   jsonify, g, redirect, session, url_for, current_app)

import requests

import mercadopago

from app.db import get_db
from app.auth import login_required
import resend


bp = Blueprint('payment', __name__, url_prefix='/payment')
PUBLIC_KEY = 'TEST-4af5bb3f-ddc6-42bb-ba38-2b245263309a'
ACCESS_TOKEN = 'TEST-2366731733437316-102122-33813790a19439f911f74ceb05890925-1519195449'

mp = mercadopago.SDK(ACCESS_TOKEN)


@bp.route("/checkout/user", methods=['GET'])
@login_required
def checkout_user():
    print("redirigiendo a la página de pagamento")
    session['cliente_id'] = g.client_id
    session['purchase_completed'] = False
    carrito = session.get('carrito', [])
    monto = 0
    cantidad_producto = {}
    items = []
    for item in carrito:
        nombre = item['nombre']
        precio = int(item['precio'])
        cantidad = int(item['cantidad'])
        monto += cantidad * precio
        cantidad_producto[item['nombre']] = cantidad

        items.append(
            {
                "title": "Productos de Mi Bello Hogar",
                "quantity": cantidad,
                "currency_id": "CLP",
                "unit_price": precio
            })

    preference = {
        "items": items,
        "back_urls": {
            "success": "http://localhost:5000/payment/success",
            "failure": "http://localhost:5000/payment/failure",
            "pending": "http://localhost:5000/payment/pending",
        },
        "notification_url": "https://5f2c-143-255-104-32.ngrok-free.app/payment/webhook",
    }

    preference_result = mp.preference().create(preference)
    preference_link = preference_result['response']['init_point']

    print("redirigiendo a la página de pago")
    print("preference_link", preference_link)
    return {"link_pago": preference_link}


@bp.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        db = get_db()
        c = db.cursor()
        c.execute("SELECT cliente_id FROM cliente WHERE email = %s", (email,))
        cliente_exists = c.fetchone()
        cliente_id = None
        if cliente_exists:
            cliente_id = cliente_exists[0]
        else:
            c.execute(
                "INSERT INTO cliente (nombre, email, telefono, direccion) VALUES (%s, %s, %s, %s)",
                (name, email, phone, address),
            )
            db.commit()
            cliente_id = c.lastrowid

        session['cliente_id'] = cliente_id
        session['purchase_completed'] = False

        return redirect(url_for('payment.payment'))

    return render_template('payment/checkout.html')


@bp.route("/", methods=['GET'])
def payment():
    carrito = session.get('carrito', [])
    monto = 0
    cantidad_producto = {}
    items = []
    for item in carrito:
        nombre = item['nombre']
        precio = int(item['precio'])
        cantidad = int(item['cantidad'])
        monto += cantidad * precio
        cantidad_producto[item['nombre']] = cantidad

        items.append(
            {
                "title": "Productos de Mi Bello Hogar",
                "quantity": cantidad,
                "currency_id": "CLP",
                "unit_price": precio
            })

    preference = {
        "items": items,
        "back_urls": {
            "success": "http://localhost:5000/payment/success",
            "failure": "http://localhost:5000/payment/failure",
            "pending": "http://localhost:5000/payment/pending",
        },
        "notification_url": "https://5f2c-143-255-104-32.ngrok-free.app/payment/webhook",
    }

    preference_result = mp.preference().create(preference)
    preference_link = preference_result['response']['init_point']

    print("redirigiendo a la página de pago")
    print("preference_link", preference_link)
    return redirect(preference_link)


@bp.route("/webhook", methods=['POST'])
def receive_webhook():
    data = request.json
    print("data", data)
    return data


@bp.route("/success", methods=['GET'])
def success_pay():
    productos = session.get('carrito', [])
    print("productos cantidad", len(productos))

    precio_total = sum(producto['precio'] * producto['cantidad']
                       for producto in productos)
    if not session.get('purchase_completed'):
        cliente_id = session.get('cliente_id')
        db = get_db()
        c = db.cursor()

        try:
            c.execute(
                "BEGIN TRANSACTION"
            )

            for producto in productos:
                nombre = producto['nombre']
                precio = producto['precio']
                cantidad = producto['cantidad']
                c.execute(
                    "UPDATE producto SET stock = stock - %s WHERE nombre_producto = %s", (
                        cantidad, nombre)
                )

            c.execute(
                "INSERT INTO compra (cliente_id, total_compra, estado) VALUES (%s, %s, %s) RETURNING compra_id", (
                    cliente_id, precio_total, 'completada')
            )

            compra_id = c.fetchone()[0]
            print("compra_id", compra_id)

            for producto in productos:
                producto_id = producto['id']
                precio = producto['precio']
                cantidad = producto['cantidad']
                c.execute(
                    "INSERT INTO detalle_compra (compra_id, producto_id, precio, cantidad) VALUES (%s, %s, %s, %s)", (
                        compra_id, producto_id, precio, cantidad)
                )

            c.execute(
                "COMMIT"
            )

            session['purchase_completed'] = True
            send(current_app.config['OWNER_MAIL'],
                 "Nueva compra desde la tienda", productos, precio_total)

            return render_template('payment/success.html', products=productos, total=precio_total)
        finally:
            c.close()
    else:
        return render_template('payment/success.html', products=productos, total=precio_total)


def send(to, subject, productos, precio_total):
    resend.api.key = current_app.config['RESEND_API_KEY']

    html_template = """
    <div style=''>
        <p><strong>¡Nueva compra desde la tienda virtual Mi Bello Hogar!</strong></p>
        <p><strong>Detalle de productos comprados:</strong></p>
        <table style='border-collapse: collapse;
        width: 60%;
        margin: auto;'>
            <tr>
                <th style='border: 1px solid black; padding: 8px;text-align: left;'>Nombre</th>
                <th style='border: 1px solid black; padding: 8px;text-align: left;'>Cantidad</th>
                <th style='border: 1px solid black; padding: 8px;text-align: left;'>Precio</th>
            </tr>
            {}
        </table>

        <p><strong>TOTAL ${}</strong></p>
    </div>
    """

    html_products = ""
    for product in productos:
        html_products += "<tr><td style='border: 1px solid black; padding: 8px;text-align: left;'>{}</td><td style='border: 1px solid black; padding: 8px;text-align: left;'>{}</td><td style='border: 1px solid black;padding: 8px; text-align: left;'>${}</td></tr>".format(
            product['nombre'], product['cantidad'], product['precio'])

    html_content = html_template.format(html_products, precio_total)
    params = {
        "from": "Mi Bello Hogar <onboarding@resend.dev>",
        "to": to,
        "subject": subject,
        "html": html_content

    }

    email = resend.Emails.send(params)


@ bp.route("/failure", methods=['GET'])
def failure_pay():
    return render_template('payment/failure.html')


@ bp.route("/pending", methods=['GET'])
def pending_pay():
    return render_template('payment/pending.html')
