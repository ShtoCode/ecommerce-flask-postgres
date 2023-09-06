from flask import Blueprint, render_template

bp = Blueprint('products', __name__, url_prefix='/productos')

@bp.route("/", methods=["GET"])
def index():
    return render_template('products/products.html')

