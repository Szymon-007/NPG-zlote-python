def calculate_ideal_tag(stress: str, motivation: str, humor: str) -> str:
    """
    Wylicza idealny tag na podstawie czystych stringów przesyłanych z frontendu.
    Wartości z Survey.jsx:
    - stress: 'niski', 'sredni', 'wysoki'
    - motivation: 'niska', 'srednia', 'wysoka'
    - humor: 'smutna', 'neutralna', 'wesola'
    """
    # Jeśli stres jest wysoki -> dajemy cytat odstresowujący
    if stress == "wysoki":
        return "odstresowujacy"

    # Jeśli motywacja jest niska -> dajemy cytat motywacyjny
    elif motivation == "niska":
        return "motywacyjny"

    # Jeśli humor jest słaby (smutna) -> dajemy cytat pocieszający
    elif humor == "smutna":
        return "pocieszajacy"

    # W każdym innym przypadku zwracamy domyślny tag
    else:
        return "ogolny"