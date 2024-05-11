from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.database.db import get_db
from src.entity.models import User
from src.schemas.user import UserSchema


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a user by their email address from the database.

    :param email: The email address of the user to retrieve.
    :param db: AsyncSession instance for database interaction.
    :return: The User object corresponding to the given email, if found; otherwise, None.
    """
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    Create a new user in the database.

    :param body: Data representing the new user.
    :param db: AsyncSession instance for database interaction.
    :return: The newly created User object.
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
   Update the refresh token of a user in the database.

   :param user: The User object to update.
   :param token: The new refresh token value (or None to clear the token).
   :param db: AsyncSession instance for database interaction.
   """
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    Confirm the email address of a user in the database.

    :param email: The email address of the user to confirm.
    :param db: AsyncSession instance for database interaction.
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    """
    Update the avatar URL of a user in the database.

    :param email: The email address of the user to update.
    :param url: The new avatar URL (or None to remove the avatar).
    :param db: AsyncSession instance for database interaction.
    :return: The updated User object.
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user
