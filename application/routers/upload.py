from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException, status, Form, Depends
from sqlalchemy.orm import Session
import base64
from .. import identifier, purchase,schemas, oauth2, database

router = APIRouter(
    tags = ['Uploading'],
    prefix = "/upload"
)

allowed_extension = {"image/png", "image/jpg", "image/jpeg"}

@router.post("/", response_model=schemas.CardDetails)
async def upload_file(file : UploadFile = File(...),
                       action : str = Form(...), db : Session = Depends(database.get_db),
                       current_user = Depends(oauth2.get_current_user)):
    if(file == None):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "No file uploaded"
        )

    if file.content_type not in allowed_extension:
        raise HTTPException(
            status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail = "File isnt an image" 
        )
    
    image_bytes = await file.read()
    # base64_image = base64.b64encode(image_bytes).decode("utf-8")
    card_details = identifier.call_llm(image_bytes)
    card_details = schemas.Card.model_validate_json(card_details)

    if(len(image_bytes) == 0):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "No file uploaded"
        )

    if(action == "buy"):
        return purchase.card_bought(card_details, db, current_user)
    else:
        return purchase.card_sold(card_details, db, current_user)