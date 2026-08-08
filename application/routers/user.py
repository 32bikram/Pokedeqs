from fastapi import status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    tags= ['user']
)

@router.post("/createuser", status_code = status.HTTP_201_CREATED, response_model = schemas.ReturnUser)
def createUser(user : schemas.GetUser, db : Session = Depends(get_db)): #getuser = pydanticschema
    existing_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_user is not None:
        raise HTTPException(
            status_code = status.HTTP_208_ALREADY_REPORTED,
            detail = "user with same credential exist"
        )
    user.password = utils.hash(user.password)
    try:
        res = models.Users(**user.model_dump())  #users = actual schema or table
        db.add(res)
        db.commit()
        db.refresh(res)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Please try again after some time"
        )
    return res


@router.get("/getuser/{email}", response_model = schemas.ReturnUser)
def getUser(email : str, db : Session = Depends(get_db)):
    res = db.query(models.Users).filter(models.Users.email == email).first()
    if res is None:
         raise HTTPException(
          status_code = status.HTTP_404_NOT_FOUND   
         )
    return res