from flask import (Blueprint, render_template, request, redirect, url_for, flash, session, g)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from app.db import get_db
import functools

bp = Blueprint('auth', __name__, url_prefix='/user')

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        phone = request.form['phone']
        addres = request.form['address']

        db = get_db()
        c = db.cursor()
        error = None
        c.execute(
            "SELECT cliente_id FROM cliente WHERE email = %s", (email,)
        )
        if not email:
            error = 'Correo es requerido'

        if not password:
            error = 'Password es requerido'
        elif c.fetchone() is not None:
            error = 'El correo {}, ya se encuentra registrado.'.format(email)

        if error is None:
            c.execute(
                'INSERT INTO cliente (nombre, email, cliente_password, telefono, direccion) VALUES (%s, %s, %s, %s, %s)', (name, email, generate_password_hash(password), phone, addres)
            )
            db.commit()
            c.execute("SELECT * FROM cliente WHERE email = %s", (email,))
            client =c.fetchone()
            db.close()
            session.clear()
            session['client_id'] = client[0]
            return redirect(url_for('store.index'))

        flash(error)
    return render_template('auth/register.html')

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['pass']
        db = get_db()
        c = db.cursor()
        error = None
        c.execute("SELECT * FROM cliente WHERE email = %s", (email,))
        client = c.fetchone()
        db.close()
        
        if client is None:
            error = "Email y/o contraseña incorrecta"
        elif not check_password_hash(client[3], password):
            error = "Email y/o contraseña incorrecta"
        
        if error is None:
            session.clear()
            session['client_id'] = client[0]
            return redirect(url_for('store.index'))
        flash(error)

    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    client_id = session.get('client_id')

    if client_id is None:
        g.client = None
    else:
        db = get_db()
        c = db.cursor()
        c.execute(
            "SELECT * FROM cliente WHERE cliente_id = %s", (client_id,)
            )
        g.client = c.fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.client is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
