from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash, session, g)
import functools
import requests
from flask_jwt_extended import decode_token
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import json
import os


bp = Blueprint('auth', __name__, url_prefix='/user')


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user = request.form['user']
        password = request.form['pass']
        phone = request.form['phone']
        addres = request.form['address']

        if not email:
            error = 'Correo es requerido'

        if not password:
            error = 'Password es requerido'

        data = {"name": name, "email": email, "user": user, "password": password,
                "telefono": phone, "direccion": addres}

        json_data = json.dumps(data)

        headers = {'Content-Type': 'application/json'}

        response = requests.post(
            'http://localhost:8000/clients/user', data=json_data, headers=headers)

        print("response", response)

        if response.status_code == 200:
            token = response.json().get('token')
            session.clear()
            session['token'] = token
            return redirect(url_for('store.index'))
        else:
            error = "Credenciales incorrectas"
            return {"error": str(error)}, 500

    return render_template('auth/register.html')


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            user = request.form['user']
            password = request.form['pass']

            data = {'user': user, 'password': password}

            json_data = json.dumps(data)

            headers = {'Content-Type': 'application/json'}

            response = requests.post(
                'http://localhost:8000/clients/login/', data=json_data, headers=headers)
            print("response", response)
            if response.status_code == 200:
                token = response.json().get('token')

                session.clear()
                session['token'] = token
                return redirect(url_for('store.index'))

            else:
                return {"error": "Credenciales incorrectas"}, 500

        except Exception as e:
            return {"error": str(e)}, 500

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    token = session.get('token')

    if token is None:
        g.authenticated = False
        g.client_id = None
    else:
        try:
            payload = decode_token(token)
            client_id = payload['sub']
            g.client_id = client_id
            g.name = payload['name']
            g.authenticated = True
        except ExpiredSignatureError:
            flash("El token JWT ha xpirado")
            g.authenticated = False
        except InvalidTokenError:
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
