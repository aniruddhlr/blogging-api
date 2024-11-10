from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from .config import JWT_SECRET_KEY
from .routes import user, post
from pydantic import BaseSettings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from the frontend
origins = [
    "http://localhost:5173",  # Allow your React frontend's URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or use ["*"] to allow all origins (but it's less secure)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# JWT Configuration
class Settings(BaseSettings):
    authjwt_secret_key: str = JWT_SECRET_KEY

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(post.router, prefix="/posts", tags=["Posts"])

@app.get("/")
async def root():
    return {"message": "Welcome to Medium Clone API"}
