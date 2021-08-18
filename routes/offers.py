from sanic import response
import sqlite3
from pydantic import BaseModel, ValidationError

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM

class Offer_id(BaseModel):
    offer_id: int

class User_id(BaseModel):
    user_id: int

def handler_offers(request):
    cursor = conn.cursor()
    offer_id = request.json.get('offer_id')
    user_id = request.json.get('user_id')

    if offer_id:
        try:
            offers = Offer_id(**{"offer_id": offer_id})
        except ValidationError as e:
            return response.json({"error": e.errors()})

        cursor.execute(f"SELECT * FROM offers WHERE id={offer_id}")
        return response.json({f"offer_{offer_id}": cursor.fetchone()})

    elif user_id:
        try:
            offers = User_id(**{"user_id": user_id})
        except ValidationError as e:
            return response.json({"error": e.errors()})

        cursor.execute(f"SELECT * FROM offers WHERE user_id={user_id}")
        return response.json({"offers": cursor.fetchall()})

    else:
        return response.json({"Message": "Use offer_id or user_id"}, status=404)
