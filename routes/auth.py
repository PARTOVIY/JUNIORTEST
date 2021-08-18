from sanic import response
import sqlite3
import jwt
import datetime
from pydantic import BaseModel, ValidationError

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM

class User(BaseModel):
    username: str
    password: str

def handler_auth(request):
    username = request.json.get('username')
    password = request.json.get('password')

    try:
        user = User(**{"username": username, "password": password})
    except ValidationError as e:
        return response.json({"error": e.errors()})

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
    for row in cursor.fetchall():
        if username == row[1] and password == row[2]:
            encoded_jwt = jwt.encode({"id": row[0], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, "secret", algorithm="HS256")
            return response.json({"id": str(row[0]), "JWT": str(encoded_jwt)[2:-1]})
        else:
            return response.json({"error": "Incorrect login or password"})
