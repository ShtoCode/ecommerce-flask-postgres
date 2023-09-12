from flask import (Blueprint, render_template, request, flash, current_app)
from app.db import get_db
import resend

bp = Blueprint('contact', __name__, url_prefix='/contacto')

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["comment"]
        db = get_db()
        c = db.cursor()
        error = None
        c.execute("SELECT COUNT(email) FROM contacto WHERE email = %s", (email,))
        email_count = c.fetchone()

        if int(email_count[0]) > 5:
            error = "Email ya ha enviado bastantes mensajes, para enviar otro porfavor espere dentro de la próxima semana"
        if error is None:
            send(current_app.config['OWNER_MAIL'], "Mensaje de un visitante en Mi Bello Hogar", message, email)
            c.execute(
                'INSERT INTO contacto (nombre, email, mensaje) VALUES (%s, %s, %s)', (name, email, message,)
                )
            db.commit()
            flashmsg = "Mensaje enviado con exito!"
            return render_template('contact/contact.html', msg=flashmsg)

        flash(error)
    
    return render_template('contact/contact.html')

def send(to, subject, content, email_visit):
    resend.api.key = current_app.config['RESEND_API_KEY']
    params = {
        "from": "Mi Bello Hogar <onboarding@resend.dev>",
        "to": to,
        "subject": subject,
        "html": "<h3 style='color:blue;'>Mensaje enviado por <strong>"+email_visit+"</strong></h3><br/><p><strong>"+content+"</strong></p>"

    }

    email = resend.Emails.send(params)