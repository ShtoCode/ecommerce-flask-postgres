from psycopg2.extras import DictCursor
from flask import current_app
import psycopg2


def get_db():
        try:
            conn = psycopg2.connect(
                host=current_app.config['DATABASE_HOST'],
                user=current_app.config['DATABASE_USER'],
                password=current_app.config['DATABASE_PASSWORD'],
                database=current_app.config['DATABASE'],
            )

            #g.c = g.db.cursor(cursor_factory=DictCursor)
            return conn
        except psycopg2.Error as e:
            print("Error de base de datos:", e)
            return None



