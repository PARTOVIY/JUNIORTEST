from crypt import methods

from sanic import Sanic
from sanic import response
import jwt
import sqlite3
import datetime
import routes

app = Sanic(__name__)
conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM

# conn.cursor().execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, email TEXT)")
# conn.cursor().execute("CREATE TABLE offers(user_id INTEGER, title TEXT, text TEXT)")

app.add_route(routes.handler_auth, '/auth', methods=["POST"])
app.add_route(routes.handler_register, '/register', methods=["POST"])
app.add_route(routes.handler_users, '/users', methods=["GET"])
app.add_route(routes.handler_create, '/create', methods=["POST"])
app.add_route(routes.handler_offers, '/offers', methods=["POST"])


app.run(host="0.0.0.0", port=8001)
