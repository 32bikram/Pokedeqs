from fastapi import FastAPI
from . import models
from .routers import upload

# models.Base.metadata.create_all(bind = engine)
app = FastAPI()
app.include_router(upload.router)

@app.get("/")
def home():
    return {
        "message" : "you are connected"
    }