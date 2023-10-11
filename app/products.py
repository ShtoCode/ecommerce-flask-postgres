from flask import Blueprint, render_template, url_for, g
from app.db import get_db
from app import cache
import requests

bp = Blueprint('products', __name__, url_prefix='/productos')


@bp.route("/", methods=["GET"])
@cache.cached()
def index():
    try:
        response_productos = requests.get(f'http://localhost:8000/products')

        if response_productos.status_code == 200:
            productos_data = response_productos.json()
            productos = productos_data.get('products', [])
            imagenes = []
            for producto in productos:
                product_id = producto.get('producto_id')
                response_imagen = requests.get(
                    f'http://localhost:8000/image/{product_id}/principal')

                if response_imagen.status_code == 200:
                    imagen_data = response_imagen.content
                    imagenes.append(
                        {'producto_id': product_id, 'imagen_data': imagen_data})
            return render_template('products/products.html', productos=productos, imagenes=imagenes, category=None)
        else:
            return {"error": "Error al obtener datos de FastAPI"}, 500

    except Exception as e:
        return {"error": str(e)}, 500


@bp.route("/<category>")
@cache.cached()
def category(category):
    try:
        response_productos = requests.get(
            f'http://localhost:8000/products/{category}')

        if response_productos.status_code == 200:
            productos_data = response_productos.json()
            productos = productos_data.get('products', [])
            imagenes = []
            for producto in productos:
                product_id = producto.get('producto_id')
                response_imagen = requests.get(
                    f'http://localhost:8000/image/{product_id}/principal')
                if response_imagen.status_code == 200:
                    imagen_data = response_imagen.content
                    imagenes.append(
                        {'producto_id': product_id, 'imagen_data': imagen_data})

            return render_template('products/products.html', productos=productos, imagenes=imagenes, category=category)
        else:
            return {"error": "Error al obtener datos de FastAPI"}, 500

    except Exception as e:
        return {"error": str(e)}, 500


@bp.route("/detalle/<producto>")
@cache.cached()
def detail(producto):
    try:
        response_producto = requests.get(
            f"http://localhost:8000/product/{producto}")

        if response_producto.status_code == 200:
            producto_data = response_producto.json()
            product = producto_data.get('product', {})
            print(product)

            product_id = product.get('producto_id')
            response_imagenes = requests.get(
                f'http://localhost:8000/images/{product_id}', stream=True)

            if response_imagenes.status_code == 200:
                imagenes = [{'producto_id': product_id, 'imagen_data': imagen_data}
                            for imagen_data in response_imagenes.iter_content(chunk_size=8192)]

                return render_template('products/detail_product.html', mueble=product, imagenes=imagenes)

        return {"error": "Error al obtener datos de FastAPI"}, 500

    except Exception as e:
        return {"error": str(e)}, 500
