from sanic import Sanic
from sanic import response
import sqlite3
import jwt
import datetime

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM

def handler_auth(request):
    username = request.json.get('username')
    if username is None:
        return response.json({'error': 'username is required'}, status=400)

    password = request.json.get('password')
    if password is None:
        return response.json({'error': 'password is required'}, status=400)

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
    for row in cursor.fetchall():
        if username == row[1] and password == row[2]:
            encoded_jwt = jwt.encode({"id": row[0], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, "secret", algorithm="HS256")
            return response.json({"id": str(row[0]), "JWT": str(encoded_jwt)[2:-1]})