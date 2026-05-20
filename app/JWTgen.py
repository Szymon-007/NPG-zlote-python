from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional


SECRET_KEY = "twoj_bardzo_tajny_i_dlugi_klucz_do_podpisywania_tokenow"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # 'exp' to standardowe pole w JWT oznaczające Expiration Time
    to_encode.update({"exp": expire})

    # Podpisanie tokena kluczem sekretnym
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt