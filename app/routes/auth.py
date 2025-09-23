from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db import get_db
from app.models import User
from app.auth import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterPayload(BaseModel):
    name: str
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=dict)
def register(payload: RegisterPayload, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    user = User(name=payload.name, email=payload.email)
    # store hashed password in a simple way: create a 'password' attribute dynamically
    user.password = get_password_hash(payload.password)
    # raw SQLAlchemy model doesn't have password column; we'll store in a separate simple table not implemented for brevity
    # For demo, create a file-based credential store (not for production)
    db.add(user)
    db.commit()
    db.refresh(user)
    # save password in a local file (dev only)
    with open(".user_credentials", "a", encoding='utf-8') as f:
        f.write(f"{user.id},{payload.email},{user.password}\n")
    return {"id": user.id, "email": user.email}

class LoginPayload(BaseModel):
    email: EmailStr
    password: str

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginPayload):
    # read credentials from local file (dev)
    try:
        with open(".user_credentials", "r", encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    matched = None
    for line in lines:
        uid, email, hashed = line.strip().split(",", 2)
        if email == payload.email:
            matched = {"id": int(uid), "email": email, "hashed": hashed}
            break
    if not matched or not verify_password(payload.password, matched["hashed"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token(data={"sub": matched["email"], "user_id": matched["id"]}, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}
