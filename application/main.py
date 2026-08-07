from fastapi import FastAPI
from . import models, database
from .routers import upload, auth, user, carddata

models.Base.metadata.create_all(bind = database.engine)
app = FastAPI()
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(user.router)
app.include_router(carddata.router)


@app.get("/")
def home():
    return {
        "message" : "you are connected"
    }