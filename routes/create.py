from sanic import response
import sqlite3
import jwt
from pydantic import BaseModel, ValidationError
from typing import List

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM


class Offer(BaseModel):
    title: str
    text: str


class ResponseError(BaseModel):
    error: List


def handler_create(request):
    auth = request.headers.get("Authorization")
    if auth is None:
        return response.json(ResponseError(error={'message': "Not Authorization"}).dict(), status=401)
    try:
        get_id = jwt.decode(auth, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return response.json(ResponseError(error={"Refresh token"}).dict())

    try:
        offer = Offer(**request.json())
    except ValidationError as e:
        return response.json(ResponseError(error={e.errors()}).dict())

    cursor = conn.cursor()
    cursor.executemany('INSERT INTO offers (user_id, title, text) VALUES (?,?,?)',
                       [(get_id["id"], offer.title, offer.text)])
    cursor.close()
    conn.commit()

    return response.json({'message': 'Success'})
