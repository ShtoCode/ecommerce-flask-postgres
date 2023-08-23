from flask import Blueprint, render_template

bp = Blueprint('contact', __name__, url_prefix='/contacto')

@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template('contact/index.html')
