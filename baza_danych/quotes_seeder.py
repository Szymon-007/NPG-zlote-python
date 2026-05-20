from sqlmodel import Session, select
from database import engine
from models import Quote, QuoteTag
 
 
QUOTES = [
    Quote(text="Najlepszym sposobem na odwdzięczenie się za uroczy moment jest cieszenie się nim.", author="Richard Bach", tag=QuoteTag.pocieszajacy),
    Quote(text="Szczęście to jedyna rzecz, która się mnoży, jeśli się ją dzieli.", author="Albert Schweitzer", tag=QuoteTag.pocieszajacy),
 
    Quote(text="Za dwadzieścia lat bardziej będziesz żałował tego, czego nie zrobiłeś, niż tego, co zrobiłeś.", author="Mark Twain", tag=QuoteTag.motywacyjny),
    Quote(text="Podróż tysiąca mil zaczyna się od jednego kroku.", author="Laozi", tag=QuoteTag.motywacyjny),
 
    Quote(text="Dobrze widzi się tylko sercem. Najważniejsze jest niewidoczne dla oczu.", author="Antoine de Saint-Exupéry", tag=QuoteTag.odstresowujacy),
    Quote(text="Najpiękniejsze rzeczy na świecie nie mogą być widziane ani dotykane – trzeba je poczuć sercem.", author="Helen Keller", tag=QuoteTag.odstresowujacy),
    
    Quote(text="Każdy nowy początek pochodzi z końca jakiegoś innego początku.", author="Seneka", tag=QuoteTag.ogolny),
    Quote(text="Prawdziwa miłość zaczyna się tam, gdzie niczego już w zamian nie oczekuje.", author="Antoine de Saint-Exupéry", tag=QuoteTag.ogolny),
]
 
 
def seed_quotes():
    print("Dodaję cytaty...")
 
    with Session(engine) as session:
        ma_cytaty = session.exec(select(Quote)).first()
 
        if ma_cytaty:
            print("Cytaty już istnieją w bazie. Pomijam.")
            return
 
        session.add_all(QUOTES)
        session.commit()
 
    print(f"Dodano {len(QUOTES)} cytatów.")
 
 
if __name__ == "__main__":
    seed_quotes()