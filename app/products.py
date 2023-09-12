from flask import Blueprint, render_template, url_for, g
from app.db import get_db

bp = Blueprint('products', __name__, url_prefix='/productos')

@bp.route("/", methods=["GET"])
def index():
    print(f"g.categorias{g.categorias}")
    return render_template('products/products.html')


@bp.route("/<category>")
def category(category):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT categoria_id FROM categoria WHERE categoria = %s", (category,))
    id = c.fetchone()
    c.execute("SELECT * FROM producto WHERE categoria_id = %s", (id,))
    productos = c.fetchall()
    print(productos)
    db.close()
    return render_template("products/products.html", productos=productos)


