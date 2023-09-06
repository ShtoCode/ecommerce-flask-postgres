from flask import (Blueprint, render_template, request,
                   flash, redirect, url_for, current_app)

from app.db import get_db

bp = Blueprint('store', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM categoria")
    categorias = c.fetchall()
    db.close()

    return render_template('store/index.html', categorias=categorias)
