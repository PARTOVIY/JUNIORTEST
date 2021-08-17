from sanic import Sanic
from sanic import response
import sqlite3
import jwt

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM

def handler_create(request):
    auth = request.headers.get("Authorization")
    if auth is None:
        return response.json({'error': 'Not authorization'}, status=401)
    try:
        get_id = jwt.decode(auth, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return response.json({"error": "Refresh Token"})

    title = request.json.get('title')
    if title is None:
        return response.json({'error': 'title is required'}, status=400)

    text = request.json.get('text')
    if text is None:
        return response.json({'error': 'text is required'}, status=400)

    cursor = conn.cursor()
    cursor.executemany('INSERT INTO offers (user_id, title, text) VALUES (?,?,?)', [(get_id["id"], title, text)])
    cursor.close()
    conn.commit()

    return response.json({'message': 'Success'})