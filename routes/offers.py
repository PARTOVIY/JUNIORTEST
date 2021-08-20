from sanic import response
import sqlite3
from pydantic import BaseModel, ValidationError
from typing import Optional, List, Dict

conn = sqlite3.connect("users.db")  # или :memory: чтобы сохранить в RAM


class ResponseOffer(BaseModel):
    id: int
    user_id: int
    title: str
    text: str

class ResponseOffers(BaseModel):
    offers: List[ResponseOffer]


class RequestSearchOffers(BaseModel):
    user_id: Optional[int] = None
    offer_id: Optional[int] = None


class ResponseError(BaseModel):
    error: Dict


def handler_offers(request):
    cursor = conn.cursor()

    try:
        request = RequestSearchOffers(**request.json)
    except ValidationError as e:
        return response.json({"error": e.errors()})

    if request.offer_id is not None:
        cursor.execute(f"SELECT * FROM offers WHERE id={request.offer_id}")
        result = cursor.fetchone()
        try:
            responsemodel = ResponseOffer(**{"id": result[0], "user_id": result[1], "title": result[2], "text": result[3]})
        except ValidationError as e:
            return response.json(ResponseError(error=e.errors()).dict())

        return response.json(responsemodel.dict())

    elif request.user_id is not None:
        cursor.execute(f"SELECT * FROM offers WHERE user_id={request.user_id}")
        result = cursor.fetchall()
        arrayres = []
        for offer in result:
            try:
                ro = ResponseOffer(**{"id": offer[0], "user_id": offer[1], "title": offer[2], "text": offer[3]})
                arrayres.append(ro)
            except ValidationError as e:
                return response.json(ResponseError(error=e.errors()).dict())

        return response.json(ResponseOffers(offers=arrayres).dict())

    else:
        return response.json(ResponseError(error={'message': "Use offer_id or user_id"}).dict(), status=404)
