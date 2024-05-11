import cloudinary
import cloudinary.uploader

from fastapi import APIRouter, Depends, UploadFile
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import User

from src.schemas.user import UserResponse
from src.services.auth import auth_service
from src.conf.config import config
from src.repository import users as repositories_users

router = APIRouter(prefix="/users", tags=["users"])
cloudinary.config(cloud_name=config.CLD_NAME, api_key=config.CLD_API_KEY, api_secret=config.CLD_API_SECRET, secure=True)


@router.get("/me", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve the currently authenticated user.

    This endpoint returns information about the currently authenticated user.

    :param user: Current authenticated user.
    :return: UserResponse object representing the authenticated user.
    """
    return user


@router.patch("/avatar", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(file: UploadFile, user: User = Depends(auth_service.get_current_user),
                           db: AsyncSession = Depends(get_db)):
    """
    Update the avatar of the authenticated user.

    This endpoint allows the authenticated user to update their avatar by uploading a new image file.

    :param file: Uploaded image file for the new avatar.
    :param user: Current authenticated user.
    :param db: AsyncSession instance for database interaction.
    :return: Updated UserResponse object with the new avatar URL.
    """
    public_id = "fine_folder/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    print(res)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get('version')
    )
    user = await repositories_users.update_avatar_url(user.email, res_url, db)
    return user
