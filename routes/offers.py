from sanic import Sanic
from sanic import response
import sqlite3

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM

def handler_offers(request):
    cursor = conn.cursor()
    offer_id = request.json.get('offer_id')
    user_id = request.json.get('user_id')

    if offer_id:
        cursor.execute(f"SELECT * FROM offers WHERE id={offer_id}")
        return response.json({f"offer_{offer_id}": cursor.fetchone()})

    elif user_id:
        cursor.execute(f"SELECT * FROM offers WHERE user_id={user_id}")
        return response.json({"offers": cursor.fetchall()})

    else:
        return response.json({"Message": "Use offer_id or user_id"}, status=404)
