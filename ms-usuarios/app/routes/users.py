from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import User, UserProfile

router = APIRouter()

@router.get("/")
def get_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return [{"id": u.id, "username": u.username, "email": u.email} for u in users]

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

@router.post("/")
def create_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    import hashlib
    user = User(username=username, email=email, password_hash=hashlib.md5(password.encode()).hexdigest())
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}

@router.get("/stats/by-country")
def users_by_country(db: Session = Depends(get_db)):
    result = db.query(UserProfile.country, func.count(UserProfile.id)).group_by(UserProfile.country).all()
    return [{"country": r[0], "count": r[1]} for r in result]
