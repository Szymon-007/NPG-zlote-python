import random
from fastapi import Depends, HTTPException
from sqlmodel import Session, select


@app.post("/losuj-cytat")
def losuj_cytat_dla_usera(
        ankieta: PollSubmit,
        baza: Session = Depends(get_db),
        aktualny_user = Depends(get_current_user)
):


    wyliczony_tag = calculate_ideal_tag(ankieta.stress, ankieta.motivation, ankieta.mood)

    wylosowany_cytat = pobierz_cytat_po_tagu_bez_powtorek7(baza, aktualny_user.id, wyliczony_tag)

    if not wylosowany_cytat:
        awaryjne_cytaty = baza.exec(select(Quote).where(Quote.tag == wyliczony_tag)).all()

        if awaryjne_cytaty:
            wylosowany_cytat = random.choice(awaryjne_cytaty)
        else:
            wszystkie_calkiem = baza.exec(select(Quote)).all()
            if wszystkie_calkiem:
                wylosowany_cytat = random.choice(wszystkie_calkiem)
            else:
                raise HTTPException(status_code=404, detail="Baza cytatów świeci pustkami!")

    zapisz_cytat_do_historii(baza, aktualny_user.id, wylosowany_cytat.id)

    return wylosowany_cytat