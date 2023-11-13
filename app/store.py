from flask import (Blueprint, render_template, request,
                   jsonify, g, redirect)

import requests

import mercadopago

bp = Blueprint('store', __name__, url_prefix='/')


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
