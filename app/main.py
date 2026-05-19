from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from sqlmodel import Field, SQLModel, Session, select, create_engine
from passlib.context import CryptContext
from pydantic import BaseModel
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
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) ->str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/reg")
def register(data: UserRegister ,baza:Session = Depends(get_db)):
    statement  = select(User).where(User.email == data.email)
    existing_User = baza.execute(statement).first()
    if existing_User:
        raise HTTPException(status_code=400, detail="Email already registered")
    haszowane= hash_password(data.password)
    nowyuz = User(name = data.name,
    email = data.email,
    password = data.password)
    baza.add(nowyuz)
    baza.commit()
    baza.refresh(nowyuz)
@app.post("/log")
def login(data:  )


@app.get("/")
def read_root():
    return FileResponse("static/index.html")
