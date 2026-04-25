from fastapi import FastAPI
from .database import engine, Base
from .routes import users
from faker import Faker
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User, UserProfile
import hashlib

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MS Usuarios", version="1.0.0")
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.on_event("startup")
async def seed_data():
    db: Session = SessionLocal()
    if db.query(User).count() < 20000:
        fake = Faker()
        print("Insertando 20,000 usuarios ficticios...")
        batch = []
        for _ in range(20000):
            user = User(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password_hash=hashlib.md5(fake.password().encode()).hexdigest(),
            )
            batch.append(user)
        db.bulk_save_objects(batch)
        db.commit()
        # Insertar perfiles
        users_db = db.query(User).all()
        profiles = []
        for u in users_db:
            profiles.append(UserProfile(
                user_id=u.id,
                country=fake.country_code(),
                bio=fake.sentence(),
            ))
        db.bulk_save_objects(profiles)
        db.commit()
        print("✅ Datos insertados")
    db.close()

@app.get("/health")
def health():
    return {"status": "ok", "service": "ms-usuarios"}
