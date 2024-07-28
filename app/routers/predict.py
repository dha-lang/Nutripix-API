from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks
from dotenv import load_dotenv, find_dotenv
from functools import wraps

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import os
import jwt
import secrets

from ..auth_bearer import JWTBearer
from ..database import SessionLocal
from ..models import TokenTable
from .auth import token_required

router = APIRouter(tags=["Predict"])

load_dotenv(find_dotenv())

ALGORITHM = os.getenv("ALGORITHM")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def token_required_predict(func):
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


def remove_file(path: str) -> None:
    os.unlink(path)


@router.post("/predict/")
@token_required
def predict_image(background_tasks: BackgroundTasks, file: UploadFile = File(...), dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)):
    FILEPATH = "./static/images/"
    filename = file.filename

    extension = filename.split(".")[1].lower()

    if extension not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="File extension is not allowed.")

    img_token = secrets.token_hex(10) + "." + extension
    generated_img_name = FILEPATH + img_token

    file_content = file.file.read()

    with open(generated_img_name, "wb") as file:
        file.write(file_content)

    base_options = python.BaseOptions(model_asset_path="model/model.tflite")

    options = vision.ImageClassifierOptions(
        base_options=base_options,
        max_results=3,
    )
    classifier = vision.ImageClassifier.create_from_options(options)

    proc_image = mp.Image.create_from_file(generated_img_name)
    result = classifier.classify(proc_image).classifications[0].categories[0]

    file.close()

    background_tasks.add_task(remove_file, generated_img_name)

    return {str(result)}
