from models import MoodEnum

def calculate_ideal_tag(stress: MoodEnum, motivation: MoodEnum, mood: MoodEnum) -> str:

    if stress == MoodEnum.bardzo_nie:
        return "odstresowujacy"


    elif motivation == MoodEnum.bardzo_nie:
        return "motywacyjny"


    elif mood == MoodEnum.bardzo_nie:
        return "pocieszajacy"


    else:
        return "ogolny cytat refleksyjny"