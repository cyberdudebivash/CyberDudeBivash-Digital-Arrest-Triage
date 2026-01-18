from hashlib import sha256
from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from .models import User
import os

SECRET_KEY = os.getenv("SECRET_KEY", "cyberdudebivash_secret_2026")
ALGORITHM = "HS256"

def get_password_hash(password: str) -> str:
    print(f"[DEBUG] Hashing password of length {len(password)} chars")
    return sha256(password.encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return sha256(plain_password.encode('utf-8')).hexdigest() == hashed_password

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, db: Session) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise JWTError
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# © 2026 CyberDudeBivash Pvt. Ltd.