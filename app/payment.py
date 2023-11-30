from flask import (Blueprint, render_template, request,
                   jsonify, g, redirect, session, url_for)

import requests

import mercadopago

from app.db import get_db


bp = Blueprint('payment', __name__, url_prefix='/payment')
PUBLIC_KEY = 'TEST-4af5bb3f-ddc6-42bb-ba38-2b245263309a'
ACCESS_TOKEN = 'TEST-2366731733437316-102122-33813790a19439f911f74ceb05890925-1519195449'

mp = mercadopago.SDK(ACCESS_TOKEN)


@bp.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if g.authenticated:
        session['cliente_id'] = g.client_id
        return redirect(url_for('payment.payment'))

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
    for item in carrito:
        precio = int(item['precio'])
        cantidad = int(item['cantidad'])
        monto += cantidad * precio
        cantidad_producto[item['nombre']] = cantidad
    print(cantidad_producto)

    preference = {
        "items": [
            {
                "title": "Productos de prueba",
                "quantity": cantidad,
                "currency_id": "CLP",
                "unit_price": monto
            }
        ],
        "back_urls": {
            "success": "http://localhost:5000/payment/success",
            "failure": "http://localhost:5000/payment/failure",
            "pending": "http://localhost:5000/payment/pending",
        },
        "notification_url": "https://5f2c-143-255-104-32.ngrok-free.app//payment/webhook",
    }

    preference_result = mp.preference().create(preference)
    print(preference_result)
    preference_link = preference_result['response']['init_point']

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

            return render_template('payment/success.html', products=productos, total=precio_total)
        finally:
            c.close()
    else:
        return render_template('payment/success.html', products=productos, total=precio_total)


@ bp.route("/failure", methods=['GET'])
def failure_pay():
    return render_template('payment/failure.html')


@ bp.route("/pending", methods=['GET'])
def pending_pay():
    return render_template('payment/pending.html')
