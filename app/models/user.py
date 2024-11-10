from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: Optional[str]
    email: EmailStr
    password: str  # Raw password input
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
