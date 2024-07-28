from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from dotenv import load_dotenv, find_dotenv
from functools import wraps

import os
import jwt

from ..utils import create_access_token, create_refresh_token, verify_password
from ..models import User, TokenTable
from ..auth_bearer import JWTBearer
from ..schemas import TokenSchema, RequestDetails

from ..database import SessionLocal


router = APIRouter(tags=["Auth"])

load_dotenv(find_dotenv())

ALGORITHM = os.getenv("ALGORITHM")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = jwt.decode(kwargs["dependencies"], JWT_SECRET_KEY, ALGORITHM)
        user_id = payload["sub"]
        data = kwargs["session"].query(TokenTable).filter_by(user_id=user_id, access_token=kwargs["dependencies"], status=True).first()

        if data:
            return func(*args, **kwargs)
        else:
            return {"message": "Token blocked"}

    return wrapper


@router.post("/login", response_model=TokenSchema)
def login(request: RequestDetails, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email!")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password!")

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = TokenTable(user_id=user.id, access_token=access, refresh_token=refresh, status=True)
    session.add(token_db)
    session.commit()
    session.refresh(token_db)

    return {
        "access_token": access,
        "refresh_token": refresh,
    }


@router.post("/logout")
@token_required
def logout(dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)):
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload["sub"]
    token_record = session.query(TokenTable).all()
    info = []
    for record in token_record:
        print("record", record)
        if (datetime.now(timezone.utc) - record.created_date).days > 1:
            info.append(record.user_id)
    if info:
        existing_token = session.query(TokenTable).where(TokenTable.user_id.in_(info)).delete()
        session.commit()

    existing_token = session.query(TokenTable).filter(TokenTable.user_id == user_id, TokenTable.access_token == token).first()
    if existing_token:
        existing_token.status = False
        session.add(existing_token)
        session.commit()
        session.refresh(existing_token)
    return {"message": "Logout Successful!"}
