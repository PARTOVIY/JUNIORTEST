from sanic import response
import sqlite3
import jwt
import datetime
from pydantic import BaseModel, ValidationError
from typing import Optional, List, Dict

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM


class User(BaseModel):
    username: str
    password: str


class ResponseOutput(BaseModel):
    ID: str
    JWT: str


class ResponseError(BaseModel):
    error: List


def handler_auth(request):

    try:
        request = User(**request.json)
    except ValidationError as e:
        return response.json(ResponseError(error=e.errors()).dict())

    try:
        user = User(**{"username": request.username, "password": request.password})
    except ValidationError as e:
        return response.json(ResponseError(error=e.errors()).dict())

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username='{request.username}'")
    results = cursor.fetchall()
    if len(results) == 0:
        return response.json(ResponseError(error={'message': "Login is not found!"}).dict())

    for row in results:
        if request.username == row[1] and request.password == row[2]:
            encoded_jwt = jwt.encode({"id": row[0], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, "secret", algorithm="HS256")
            return response.json(ResponseOutput(ID=row[0], JWT=str(encoded_jwt)[2:-1]).dict())
        else:
            return response.json(ResponseError(error={'message': "Incorrect login or password"}).dict())
