from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from .models import Base, User, Report
from .database import engine, get_db
from .security import create_access_token, verify_password, get_password_hash, verify_token
from .triage import triage_digital_arrest
from .utils import sanitize_input
from .ai_model import calculate_risk_score
from pydantic import BaseModel
import os

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CyberDudeBivash Digital Arrest Triage Script", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserIn(BaseModel):
    username: str
    password: str

class TriageIn(BaseModel):
    transcript: str
    url: str = None
    image_url: str = None
    language: str = "en"

class TriageOut(BaseModel):
    risk_score: float
    indicators: list[str]
    advice: str
    report_id: int

@app.post("/register")
def register(user: UserIn, db: Session = Depends(get_db)):
    print(f"[DEBUG] Register attempt started - username: '{user.username}', password length: {len(user.password)} chars")
    try:
        hashed_password = get_password_hash(user.password)
        print("[DEBUG] Password hashed successfully")
        new_user = User(username=user.username, hashed_password=hashed_password)
        db.add(new_user)
        print("[DEBUG] User added to session")
        db.commit()
        print("[DEBUG] Commit succeeded")
        db.refresh(new_user)
        print("[DEBUG] User refreshed")
        return {"username": new_user.username}
    except Exception as e:
        db.rollback()
        error_msg = f"Registration failed: {str(e)}"
        print(f"[ERROR] {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"[DEBUG] Login attempt for username: {form_data.username}")
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        print("[ERROR] Invalid credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": user.username}, timedelta(minutes=30))
    print("[DEBUG] Login successful - token generated")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/triage", response_model=TriageOut)
def perform_triage(input: TriageIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("[DEBUG] Triage request received")
    user = verify_token(token, db)
    sanitized = sanitize_input(input.transcript)
    indicators = triage_digital_arrest(sanitized, input.url, input.image_url, input.language)
    risk_score = calculate_risk_score(indicators)
    advice = "HIGH RISK - Report immediately to 1930 or cybercrime.gov.in" if risk_score > 50 else "Low risk detected, but remain vigilant."
    try:
        report = Report(user_id=user.id, transcript=sanitized, risk_score=risk_score, advice=advice)
        db.add(report)
        db.commit()
        db.refresh(report)
        print("[DEBUG] Triage report saved successfully")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to save report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save report: {str(e)}")
    
    return {
        "risk_score": risk_score,
        "indicators": indicators,
        "advice": advice,
        "report_id": report.id
    }

@app.get("/health")
def health():
    return {"status": "healthy", "authority": "CyberDudeBivash™"}

print("[INFO] Application loaded successfully")

# © 2026 CyberDudeBivash Pvt. Ltd.