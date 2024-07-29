from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import auth, user, predict


description = """
NutriPix API is an API based on the NutriPix App.

List of operations you can do :

**Auth:**
- Login.
- Logout.

**Users:**
- Register.
- Change Password.
- Get User Data.

**Prediction:**
- Post Prediction.
"""

tags_metadata = [
    {
        "name": "User",
        "description": "Operations related to user, such as register and password change.",
    },
    {
        "name": "Auth",
        "description": "Operations related to user authentication and authorization, such as login and logout.",
    },
    {
        "name": "Predict",
        "description": "Operations related to prediction.",
    },
]

app = FastAPI(
    title="NutriPix API",
    description=description,
    version="0.1.0",
    openapi_tags=tags_metadata,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(engine)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(predict.router)


@app.get("/")
def root():
    return {"message": "Welcome to NutriPix API!"}
