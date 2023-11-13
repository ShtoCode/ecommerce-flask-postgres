from flask import (Blueprint, render_template, request,
                   jsonify, g, redirect)

import requests

import mercadopago


bp = Blueprint('payment', __name__, url_prefix='/payment')
PUBLIC_KEY = 'TEST-4af5bb3f-ddc6-42bb-ba38-2b245263309a'
ACCESS_TOKEN = 'TEST-2366731733437316-102122-33813790a19439f911f74ceb05890925-1519195449'

mp = mercadopago.SDK(ACCESS_TOKEN)


@bp.route("/", methods=['POST'])
def payment():
    data = request.get_json()
    carrito = data['carrito']
    monto = 0
    cantidad_producto = {}
    for item in carrito:
        precio = int(item['precio'])
        cantidad = int(item['cantidad'])
        monto += cantidad * precio
        cantidad_producto[item['nombre']] = cantidad

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
        "notification_url": "https://eeee-143-255-104-32.ngrok-free.app/payment/webhook",
    }
    preference_result = mp.preference().create(preference)
    preference_link = preference_result['response']['init_point']

    return jsonify({"pagina_pago": preference_link})


@bp.route("/webhook", methods=['POST'])
def receive_webhook():
    data = request.json
    print(data)
    return data


@bp.route("/success", methods=['GET'])
def success_pay():
    return render_template('payment/success.html')


@bp.route("/failure", methods=['GET'])
def failure_pay():
    return render_template('payment/failure.html')


@bp.route("/pending", methods=['GET'])
def pending_pay():
    return render_template('payment/pending.html')
