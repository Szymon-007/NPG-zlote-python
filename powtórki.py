from datetime import date, timedelta
from sqlmodel import select, Session


def get_blacklisted_quotes(user_id: int, db: Session) -> list[int]:
    fourteen_days_ago = date.today() - timedelta(days=14)

    statement = select(QuoteHistory.quote_id).where(
        QuoteHistory.user_id == user_id,
        QuoteHistory.created_date >= fourteen_days_ago
    )

    results = db.exec(statement).all()

    return results