from sqlmodel import Session, SQLModel, create_engine
from models import User, Quote, QuoteHistory

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
    echo=True
)
def stworz_tabele():
    SQLModel.metadata.create_all(engine)

def pobierz_sesje():
    with Session(engine) as sesja:
        yield sesja

if __name__ == "__main__":
    stworz_tabele()
    print(" Baza danych i wszystkie tabele zostały pomyślnie utworzone!")