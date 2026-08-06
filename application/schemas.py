from pydantic import BaseModel, EmailStr, ConfigDict

class Card(BaseModel):
        pokemon_name : str
        card_name : str
        set_name : str
        card_number : str
        card_id : str | None = None

        model_config = ConfigDict(from_attributes=True)
        #if the input is an object dont expect dictionary, read the atributes, 
        #works for sqlorm since it return obj not json or dict

class CardDetails(Card):
        card_count : int

class GetUser(BaseModel):
        email : EmailStr
        password : str

class User(BaseModel):
        email : EmailStr

class ReturnUser(User):
        pass

class TokenData(BaseModel):
        id : int 

class JwtData(BaseModel):
        access_token : str
        token_type : str