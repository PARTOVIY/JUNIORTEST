from sanic import response
import sqlite3
from pydantic import BaseModel, ValidationError, EmailStr

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM


class User(BaseModel):
    username: str
    password: str
    email: EmailStr


def handler_register(request):
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    try:
        user = User(**{"username": username, "password": password, "email": email})
    except ValidationError as e:
        return response.json({"error": e.errors()})

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE email='{email}'")
    if cursor.fetchone() is not None:
        return response.json({'error': 'email is busy'}, status=400)

    cursor = conn.cursor()
    cursor.executemany('INSERT INTO users (username, password, email) VALUES (?,?,?)', [(username, password, email)])
    cursor.close()
    conn.commit()

    return response.json({'message': 'Success'})
