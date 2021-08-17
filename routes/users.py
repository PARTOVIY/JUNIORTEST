from sanic import Sanic
from sanic import response
import sqlite3
import jwt

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM

def handler_users(request):
    auth = request.headers.get("Authorization")
    if auth is None:
        return response.json({'error': 'Not authorization'}, status=401)
    try:
        get_id = jwt.decode(auth, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return response.json({"error": "Refresh Token"})

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users JOIN offers ON users.id={get_id['id']} AND users.id=offers.user_id")
    results = cursor.fetchall()
    offers_array = []
    for offer in results:
        offers_array.append(offer[4:])

    for user in results:
        return response.json({
            "id": user[0],
            "username": str(user[1]),
            "email": str(user[3]),
            "offers": offers_array
        })