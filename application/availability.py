#CHECKS IF A CARD IS AVAILABLE IF NOT CREATES ENTRY FOR THAT CARD
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, database, oauth2, schemas

def card_exist(card : schemas.Card, db : Session, current_user : models.Users):
        set_name = card.set_name.strip().lower().replace(" ", "_")
        card_id = f"{set_name}-{card.card_number}"
        if(card.card_id==None):
                card.card_id = card_id

        res = db.query(models.Collections).filter(models.Collections.card_id==card_id,
        models.Collections.user_id==current_user.user_id).first()
        if(res==None):
        #that card has no relation with that user
        #create the card entry
                try:
                        card_detail = db.query(models.Cards).filter(models.Cards.card_id==card_id).first()
                        if(card_detail==None):
                                new_card = models.Cards(**card.model_dump())
                                db.add(new_card)
                                db.commit()
                                db.refresh(new_card)
                        new_collection = models.Collections(card_id = card_id, user_id = current_user.user_id, card_count=0)
                        db.add(new_collection)
                        db.commit()
                        db.refresh(new_collection)
                except:
                        raise HTTPException(
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Please try again after some time (exist check)"
                        )
        return True