from sanic import response
import sqlite3
from pydantic import BaseModel, ValidationError
from typing import Optional, List

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM


class ResponseUser(BaseModel):
    user_id: int


class ResponseOffer(BaseModel):
    id: int


class ResponseOffers(BaseModel):
    offers: List[ResponseOffer]


class RequestSearchOffers(BaseModel):
    user_id: Optional[int] = None
    offer_id: Optional[int] = None


class ResponseSearchOffers(BaseModel):
    users: Optional[List[ResponseUser]]
    offers: Optional[List[ResponseOffers]]


class ResponseError(BaseModel):
    error: str


def handler_offers(request):
    cursor = conn.cursor()

    try:
        request = RequestSearchOffers(**request.json)
    except ValidationError as e:
        return response.json({"error": e.errors()})

    if request.offer_id is not None:
        cursor.execute(f"SELECT * FROM offers WHERE id={request.offer_id}")
        return response.json({f"offer_{request.offer_id}": cursor.fetchone()})

    elif request.user_id is not None:
        cursor.execute(f"SELECT * FROM offers WHERE user_id={request.user_id}")
        return response.json({"offers": cursor.fetchall()})

    else:
        return response.json(ResponseError(error="Use offer_id or user_id").dict(), status=404)
