from fastapi import FastAPI
from . import models

# models.Base.metadata.create_all(bind = engine)
app = FastAPI()

@app.get("/")
def home():
    return {
        "message" : "you are connected"
    }