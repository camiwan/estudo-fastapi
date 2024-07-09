from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.userModel import UserModel
from app.schemas.user import UserCreate, User, PassWordChange
from passlib.context import CryptContext
from typing import List

user_router = APIRouter()

pw_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_pw_hash(password):
    return pw_context.hash(password)

def verify_pw(plain_password, hashed_password):
    return pw_context.verify(plain_password, hashed_password)

@user_router.get('/', response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@user_router.post('/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    
    hashed_password = get_pw_hash(user.password)
    new_user = UserModel(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@user_router.post('/login')
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail='Invalid email or password')
    
    if not verify_pw(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail='Invalid email or password')
    
    return {'message': 'Login sucessful'}

@user_router.put('/change-password')
def change_password(user_id: int, passwords: PassWordChange, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    if not verify_pw(passwords.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail='Old password is incorrect')

    user.hashed_password = get_pw_hash(passwords.new_password)
    db.commit()

    return {'message': 'Password updated successfully'}


