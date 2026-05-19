
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlmodel import SQLModel, select
from passlib.context import CryptContext
from bas import get_db, User, engine
from models import UserLogin, UserRegister

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()



@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/reg")
def register(data: UserRegister, baza: Session = Depends(get_db)):
    statement = select(User).where(User.email == data.email)
    existing_user = baza.execute(statement).scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Wygenerowanie hasha z odebranego jawnego hasła
    haszowane = hash_password(data.password)

    # Inicjalizacja nowego obiektu w bazie (zostało tu naprawione przypisanie hasła)
    nowyuz = User(
        name=data.name,
        email=data.email,
        hashed_password=haszowane
    )
    baza.add(nowyuz)
    baza.commit()
    baza.refresh(nowyuz)

    return {"message": "User registered successfully", "user_id": nowyuz.id}


@app.post("/log")
def login(data: UserLogin, baza: Session = Depends(get_db)):
    statement = select(User).where(User.email == data.email)
    user = baza.execute(statement).scalars().first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return {"message": "Logged in successfully", "user_id": user.id}



if __name__ == "__main__":
    create_db_and_tables()
    print("Baza danych i tabela User zostały pomyślnie utworzone!")

    test_hash = hash_password("SuperTajneHaslo123")
    print(f"Przykładowy hash dla Twojego hasła: {test_hash}")