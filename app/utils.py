from sqlalchemy.orm import Session
from app import models, auth

def create_initial_user(db: Session):
    user = db.query(models.User).filter(models.User.username == "admin").first()
    if not user:
        hashed_password = auth.get_password_hash("admin")
        db_user = models.User(username="admin", hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print("Initial user 'admin' created.")
    else:
        print("Initial user 'admin' already exists.")
