#HANDLES PURCHASE AND SELLING
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, database, availability, models, oauth2

def card_bought(card : schemas.Card, db : Session, current_user : models.Users):
    set_name = card.set_name.strip().lower().replace(" ", "_")
    card_id = f"{set_name}-{card.card_number}"

    if(availability.card_exist(card, db, current_user)==True):
        card_data = db.query(models.Collections).filter(models.Collections.card_id==card_id,
                                                        models.Collections.user_id==current_user.user_id).first()
        if card_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card not found in collection."
            )
        card_data.card_count += 1
        db.commit()
        db.refresh(card_data)
        try:
            card_details = (
                db.query(models.Cards, models.Collections.card_count)
                .join(
                    models.Collections,
                    models.Cards.card_id == models.Collections.card_id
                )
                .filter(
                    models.Cards.card_id == card.card_id,
                    models.Collections.user_id == current_user.user_id
                )
                .first()
            )
        except:
            print("error in card bought")
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = "Please try again after some time"
            )
    card_obj, count = card_details
    data = schemas.Card.model_validate(card_obj).model_dump()
    data["card_count"] = count
    return schemas.CardDetails(**data)


def card_sold(card : schemas.Card, db : Session, current_user : models.Users):
    set_name = card.set_name.strip().lower().replace(" ", "_")
    card_id = f"{set_name}-{card.card_number}"

    card_data = (db.query(models.Collections).filter
    (models.Collections.card_id==card_id,models.Collections.user_id==current_user.user_id).first())

    if card_data is None:
        print("problem in purchaase line 54")
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card not found in collection."
            )
    
    if(card_data.card_count==0):
        raise HTTPException(
            status_code = status.HTTP_204_NO_CONTENT,
            detail = "you have 0 amount of this card"
        )
    
    card_data.card_count -= 1
    db.commit()
    db.refresh(card_data)

    try:
        card_details = (
                db.query(models.Cards, models.Collections.card_count)
                .join(
                    models.Collections,
                    models.Cards.card_id == models.Collections.card_id
                )
                .filter(
                    models.Cards.card_id == card_id,
                    models.Collections.user_id == current_user.user_id
                )
                .first()
        )
    except:
        print("error in card sell")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Please try again after some time"
        )
    if(card_details==None):
        raise HTTPException(
            status_code = status.HTTP_204_NO_CONTENT,
            detail = "there is 0 of this card in inventory"
        )
    
    card_obj, count = card_details
    data = schemas.Card.model_validate(card_obj).model_dump()
    data["card_count"] = count
    return schemas.CardDetails(**data)