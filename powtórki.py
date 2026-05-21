def pobierz_cytat_po_tagu_bez_powtorek14(sesja: Session, user_id: int, tag: QuoteTag) -> Optional[Quote]:

    dwa_tygodnie_temu = datetime.now() - timedelta(days=14)

    history_stmt = select(QuoteHistory.quote_id).where(
        QuoteHistory.user_id == user_id,
        QuoteHistory.received_at >= dwa_tygodnie_temu
    )

    recent_quote_ids = sesja.exec(history_stmt).all()

    stmt = select(Quote).where(Quote.tag == tag)

    if recent_quote_ids:
        stmt = stmt.where(Quote.id.notin_(recent_quote_ids))

    available_quotes = sesja.exec(stmt).all()

    if not available_quotes:
        return None

    return git andom.choice(available_quotes)