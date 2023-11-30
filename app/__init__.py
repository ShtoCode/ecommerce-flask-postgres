import os
import base64
import requests

from flask import Flask, g
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager

cache = Cache(config={"CACHE_TYPE": "SimpleCache",
              "CACHE_DEFAULT_TIMEOUT": 48*60*60})

cors = CORS(resources={r"/payment": {"origins": "https://www.mercadopago.cl"}})


def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    cache.init_app(app)
    cors.init_app(app)
    JWTManager(app)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE_HOST=os.environ.get('DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('DATABASE_USER'),
        DATABASE=os.environ.get('DATABASE'),
        RESEND_API_KEY=os.environ.get('RESEND_API_KEY'),
        OWNER_MAIL=os.environ.get('OWNER_MAIL')

    )

    from . import store
    from . import contact
    from . import products
    from . import auth
    from . import payment

    from .db import get_db

    def b64encode_filter(data):
        return base64.b64encode(data).decode('utf-8')

    app.jinja_env.filters['b64encode'] = b64encode_filter

    @app.before_request
    def before_request():
        try:
            response = requests.get("http://127.0.0.1:8000/categorys/display")
            if response.status_code == 200:
                data = response.json()
                g.categorias = data
        except:
            return {"error": "Error al obtener datos de FastAPI"}, 500

    app.register_blueprint(store.bp)
    app.register_blueprint(contact.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(payment.bp)

    return app
