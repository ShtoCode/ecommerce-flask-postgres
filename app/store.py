from flask import (Blueprint, render_template, request,
                jsonify, g, redirect)

import requests

import mercadopago


bp = Blueprint('store', __name__, url_prefix='/')

PUBLIC_KEY = 'TEST-4af5bb3f-ddc6-42bb-ba38-2b245263309a'
ACCESS_TOKEN = 'TEST-2366731733437316-102122-33813790a19439f911f74ceb05890925-1519195449'

mp = mercadopago.SDK(ACCESS_TOKEN)


@bp.route('/', methods=['GET'])
def index():
    try:
        response = requests.get("http://127.0.0.1:8000/categorys")
        if response.status_code == 200:
            data = response.json()
            return render_template('store/index.html', categorias=data)
        else:
            return {"error": "Error al obtener datos de FastAPI"}, 500

    except Exception as e:
        return {"error": str(e)}, 500
    

@bp.route("/carrito", methods=['GET'])
def cart():
    return render_template('store/carrito.html')

@bp.route("/delivery", methods=["GET", "POST"])
def delivery():
    if g.authenticated == True:
        return "registrado ajjaja hola crak"
    else:

        return render_template('store/delivery.html')
    
@bp.route("/payment", methods=['POST'])
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
        "items":[
            {
            "title": "Productos de prueba",
            "quantity": cantidad,
            "currency_id": "CLP",
            "unit_price": monto
        }
        ],
        "back_urls": {
            "success": "http://localhost:5000/success",
            "failure": "http://localhost:5000/failure",
            "pending": "http://localhost:5000/pending",
        },
        "notification_url": "https://ead8-143-255-104-32.ngrok-free.app/webhook",
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
    return "Pago realizado con exito"

@bp.route("/failure", methods=['GET'])
def failure_pay():
    return "No se pudo procesar tu pago :("

@bp.route("/pending", methods=['GET'])
def pending_pay():
    return "Tu pago está pendiente"



