from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func #for fuzzy search
from .. import database, oauth2, models, schemas

router = APIRouter(
    tags = ['Carddata'],
    prefix = "/search"
)

@router.get("/")
def get_card_data(pokemon_name : Optional[str] = None, set_name : Optional[str] = None, 
                db : Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_user)):
    
    if(pokemon_name is None) == (set_name is None):
        return {
            "response" : "please enter one value, either pokemon name or set name"
        }

    if(pokemon_name!=None):
        card_details = (db.query(models.Cards, models.Collections.card_count).
            join(models.Collections, models.Cards.card_id==models.Collections.card_id)
            .filter(models.Collections.user_id==current_user.user_id,
            func.similarity(models.Cards.pokemon_name,pokemon_name) > 0.3)
            .order_by(func.similarity(models.Cards.pokemon_name, pokemon_name).desc()).all())

        if(card_details==None):
            raise HTTPException(
                status_code =  status.HTTP_204_NO_CONTENT,
                detail = "no data about this pokemon"
            )
        card_data = []
        for cards in card_details:
            card_obj, card_count = cards
            data = schemas.Card.model_validate(card_obj).model_dump()
            data["card_count"] = card_count
            card_data.append(data)
        return card_data

    if(set_name!=None):
        card_details = (db.query(models.Cards, models.Collections.card_count).
        join(models.Collections, models.Cards.card_id==models.Collections.card_id)
        .filter(models.Collections.user_id==current_user.user_id,
        func.similarity(models.Cards.set_name,set_name) > 0.3)
        .order_by(func.similarity(models.Cards.set_name, set_name).desc()).all())
        
        if(card_details==None):
            raise HTTPException(
                    status_code =  status.HTTP_204_NO_CONTENT,
                    detail = "no data about this pokemon"
                )
        card_data = []
        for cards in card_details:
            card_obj, card_count = cards
            data = schemas.Card.model_validate(card_obj).model_dump()
            data["card_count"] = card_count
            card_data.append(data)

        return card_data