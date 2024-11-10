from fastapi import APIRouter, HTTPException, Depends
from ..models.user import User
from ..database import get_collection
from ..config import JWT_SECRET_KEY
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

router = APIRouter()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Token creation function
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt

@router.post("/signup")
async def signup(user: User):
    users_collection = await get_collection("users")
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = user.dict()
    user_dict["hashed_password"] = hash_password(user.password)
    
    await users_collection.insert_one(user_dict)
    return {"msg": "User created successfully"}

@router.post("/login")
async def login_for_access_token(user: User):
    users_collection = await get_collection("users")
    db_user = await users_collection.find_one({"email": user.email})
    
    # Check if the user exists and if the password is correct
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):  # Use user.password here
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
