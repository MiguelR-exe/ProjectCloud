from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from ..database import get_db
from ..models import User, UserProfile
import hashlib

router = APIRouter()

class RegisterBody(BaseModel):
    username: str
    email: str
    password: str

class LoginBody(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(body: RegisterBody, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(status_code=400, detail="Username ya en uso")
    user = User(
        username=body.username,
        email=body.email,
        password_hash=hashlib.md5(body.password.encode()).hexdigest(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username, "email": user.email}

@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or user.password_hash != hashlib.md5(body.password.encode()).hexdigest():
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {"id": user.id, "username": user.username, "email": user.email}

@router.get("/stats/by-country")
def users_by_country(db: Session = Depends(get_db)):
    result = db.query(UserProfile.country, func.count(UserProfile.id)).group_by(UserProfile.country).all()
    return [{"country": r[0], "count": r[1]} for r in result]

@router.get("/")
def get_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return [{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "country": u.profile.country if u.profile else None,
    } for u in users]

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "profile": {
            "country": user.profile.country if user.profile else None,
            "bio": user.profile.bio if user.profile else None,
        }
    }
