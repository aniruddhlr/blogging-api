from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from ..models.post import Post
from ..database import get_collection

router = APIRouter()

@router.post("/create")
async def create_post(post: Post, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    user_email = Authorize.get_jwt_subject()
    post_dict = post.dict()
    post_dict["author_id"] = user_email

    posts_collection = await get_collection("posts")
    result = await posts_collection.insert_one(post_dict)
    return {"msg": "Post created", "post_id": str(result.inserted_id)}

@router.get("/{post_id}")
async def get_post(post_id: str):
    posts_collection = await get_collection("posts")
    post = await posts_collection.find_one({"_id": post_id})
    if post:
        return post
    raise HTTPException(status_code=404, detail="Post not found")
