from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import token_required
from ..utils import verify_password, get_hashed_password
from ..models import User
from ..auth_bearer import JWTBearer
from ..schemas import UserCreate, ChangePassword

from ..database import SessionLocal

router = APIRouter(tags=["User"])


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.get("/get-users")
@token_required
def get_users(dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)):
    user = session.query(User).all()
    return user


@router.post("/register")
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_pass = get_hashed_password(user.password)

    new_user = User(username=user.username, email=user.email, password=encrypted_pass)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User created successfully!"}


@router.post("/change-password")
def change_password(request: ChangePassword, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == request.email).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found!")

    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password!")

    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    session.commit()

    return {"message": "Password changed successful!"}
