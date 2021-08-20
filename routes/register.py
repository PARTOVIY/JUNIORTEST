from sanic import response
import sqlite3
from pydantic import BaseModel, ValidationError, EmailStr
from typing import List

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM


class User(BaseModel):
    username: str
    password: str
    email: EmailStr


class ResponseError(BaseModel):
    error: List


def handler_register(request):
    try:
        user = User(**{"username": request.username, "password": request.password, "email": request.email})
    except ValidationError as e:
        return response.json(ResponseError(error={e.errors()}).dict())

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE email='{request.email}'")
    if cursor.fetchone() is not None:
        return response.json(ResponseError(error={"Email is busy!"}).dict(), status=400)

    cursor = conn.cursor()
    cursor.executemany('INSERT INTO users (username, password, email) VALUES (?,?,?)', [(request.username, request.password, request.email)])
    cursor.close()
    conn.commit()

    return response.json({'message': 'Success'})
