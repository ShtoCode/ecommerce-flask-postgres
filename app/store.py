from flask import (Blueprint, render_template, request,
                   flash, redirect, url_for, current_app)

from app.db import get_db

bp = Blueprint('store', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():

    return render_template('store/index.html')

