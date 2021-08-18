from sanic import response
import sqlite3
import jwt
from pydantic import BaseModel, ValidationError

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM

class Offer(BaseModel):
    title: str
    text: str

def handler_create(request):
    auth = request.headers.get("Authorization")
    if auth is None:
        return response.json({'error': 'Not authorization'}, status=401)
    try:
        get_id = jwt.decode(auth, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return response.json({"error": "Refresh Token"})

    title = request.json.get('title')
    text = request.json.get('text')

    try:
        offer = Offer(**{"title": title, "text": text})
    except ValidationError as e:
        return response.json({"error": e.errors()})

    cursor = conn.cursor()
    cursor.executemany('INSERT INTO offers (user_id, title, text) VALUES (?,?,?)', [(get_id["id"], title, text)])
    cursor.close()
    conn.commit()

    return response.json({'message': 'Success'})