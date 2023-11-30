from flask import (Blueprint, render_template, request,
                   jsonify, g, redirect, url_for, session)

import requests

import mercadopago

bp = Blueprint('store', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
    try:
        response = requests.get("http://127.0.0.1:8000/categorys/display")
        products = requests.get("http://127.0.0.1:8000/products")
        if response.status_code == 200 and products.status_code == 200:
            data = response.json()
            products = products.json()
            productos = products.get('products', [])
            imagenes = []
            for producto in productos:
                product_id = producto.get('producto_id')
                response_imagen = requests.get(
                    f'http://localhost:8000/image/{product_id}/principal')
                if response_imagen.status_code == 200:
                    imagen_data = response_imagen.content
                    imagenes.append(
                        {'producto_id': product_id, 'imagen_data': imagen_data})

            return render_template('store/index.html', categorias=data, productos=productos, imagenes=imagenes)
        else:
            return {"error": "Error al obtener datos de FastAPI"}, 500

    except Exception as e:
        return {"error": str(e)}, 500


@ bp.route("/carrito", methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        data = request.get_json()
        carrito = data['carrito']
        session['carrito'] = carrito
        print("PRODUCTOS EN SESSION", session["carrito"])
        return redirect(url_for('payment.checkout'))
    return render_template('store/carrito.html')
