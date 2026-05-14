from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from starlette.responses import FileResponse

from base_engine import get_db, base, engine
from schemat import *
from fastapi.middleware.cors import CORSMiddleware
from base import User
from fastapi.staticfiles import StaticFiles
app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
def register(data: UserRegister ,baza:Session = Depends(get_db)):
    nowyuz = User(name = data.name,
    email = data.email,
    password = data.password)
    baza.add(nowyuz)
    baza.commit()
    baza.refresh(nowyuz)



@app.get("/")
def read_root():
    return FileResponse("static/index.html")
