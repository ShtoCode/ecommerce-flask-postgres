import os

from flask import Flask, g


def create_app():
    app = Flask(__name__)

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

    from .db import get_db


    @app.before_request
    def before_request():
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM categoria")
        g.categorias = c.fetchall()
        db.close()


    app.register_blueprint(store.bp)
    app.register_blueprint(contact.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(auth.bp)

    return app
