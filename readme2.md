[3.7] models.py Modele dla minek i weryfikacja statusu: Wjechały odpowiednie modele (Pydantic i SQLModel) pod odpowiedzi z frontu (PollSubmit z użyciem MoodEnum). Sprawdzanie, czy ankieta była już dzisiaj klikana, opieramy po prostu na tym, czy user ma wpis w tabeli QuoteHistory z dzisiejszą datą. Nie trzymamy samych ankiet w bazie.

[3.8] utils.py Logika wyliczania idealnego tagu: Napisany został silnik (drzewko if/elif/else), który trawi minki od usera. Największą wagę ma stres (zwraca "odstresowujacy"), potem motywacja, a na końcu samopoczucie. Jak wszystko jest na plusie, leci tag domyślny.

[3.9] Logika zapobiegania powtórkom (Blacklista): Żeby nie robić wam konfliktów w crud.py, zrezygnowałem z pisania własnego zapytania na 14 dni. Endpoint używa Waszej gotowej funkcji pobierz_cytat_po_tagu_bez_powtorek7. Odrzucamy powtórki z ostatniego tygodnia.

[3.10] wybieraniecytatu.py Bezpiecznik (Fallback): Został wbudowany bezpośrednio w główny endpoint, żeby nie ruszać Waszego pliku crud.py. Jeśli pula świeżych cytatów dla danego tagu się wyczerpie (Wasza funkcja zwróci None), system zrzuca filtry i losuje cytat na ślepo z całej bazy, żeby front nigdy nie dostał pustego ekranu.

[3.11] wybieraniecytatu.py Główny endpoint losujący (/losuj-cytat): Serce całego modułu. Endpoint odbiera token JWT (wiemy, kto klika), przyjmuje minki z ankiety, wylicza tag, odpala losowanie (z bezpiecznikiem z 3.10) i zapisuje do bazy wyłącznie wynik (zapisz_cytat_do_historii). Same minki idą do śmieci, zgodnie z ustaleniami od Scrum Mastera.

[3.12] ratunek.py  Globalny łapacz błędów bazy (Exception Handler): Polisa ubezpieczeniowa dla apki. Zrobiłem w main.py globalny handler na SQLAlchemyError. Jak tylko padnie połączenie z SQLite, apka nie sypie stack tracem na lewo i prawo, tylko elegancko i bezpiecznie zwraca na front kod 500 z miłym komunikatem o usterce.