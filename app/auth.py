from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash, session, g)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from app.db import get_db
import functools
import requests
import jwt
import json
import os


bp = Blueprint('auth', __name__, url_prefix='/user')


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        phone = request.form['phone']
        addres = request.form['address']

        if not email:
            error = 'Correo es requerido'

        if not password:
            error = 'Password es requerido'

        data = {"name": name, "email": email, "password": password,
                "telefono": phone, "direccion": addres}

        json_data = json.dumps(data)

        headers = {'Content-Type': 'application/json'}

        response = requests.post(
            'http://localhost:8000/clients/', data=json_data, headers=headers)
        
        if response.status_code == 200:
            token = response.json().get('token')
            session.clear()
            session['token'] = token
            return redirect(url_for('store.index'))
        else:
            error = "Hubo un error al crear la cuenta, porfavor intenta más tarde"

        flash(error)
    return render_template('auth/register.html')


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form['email']
            password = request.form['pass']

            data = {'email': email, 'password': password}

            json_data = json.dumps(data)

            headers = {'Content-Type': 'application/json'}

            response = requests.post(
                'http://localhost:8000/clients/login/', data=json_data, headers=headers)

            if response.status_code == 200:
                token = response.json().get('token')

                session.clear()
                session['token'] = token
                return redirect(url_for('store.index'))

            else:
                error = "Email y/o contraseña incorrecta"
                flash(error)

        except Exception as e:
            return {"error": str(e)}, 500

    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    token = session.get('token')

    if token is None:
        g.authenticated = False
    else:
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            g.authenticated = True
        except jwt.ExpiredSignatureError:
            flash("El token JWT ha expirado")
            g.authenticated = False
        except jwt.InvalidTokenError:
            flash("Token JWT inválido")
            g.authenticated = False



def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.authenticated == False:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
