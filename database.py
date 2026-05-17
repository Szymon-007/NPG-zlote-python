from typing import Optional
from sqlmodel import Field, SQLModel, create_engine
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Zamienia czyste hasło na bezpieczny hash kryptograficzny."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Sprawdza, czy wpisane hasło zgadza się z hashem zapisanym w bazie (przyda się przy logowaniu)."""
    return pwd_context.verify(plain_password, hashed_password)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
    print("Baza danych i tabela User zostały pomyślnie utworzone!")

    test_hash = hash_password("SuperTajneHaslo123")
    print(f"Przykładowy hash dla Twojego hasła: {test_hash}")