from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.entity.models import User
from src.schemas.schemas import TagModel, TagResponse
from src.repository import tags as repository_tags
from src.services.auth import auth_service

router = APIRouter(prefix='/tags', tags=["tags"])


@router.get("/", response_model=List[TagResponse])
async def read_tags(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db),
                    user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a list of tags.

    :param skip: Number of tags to skip.
    :param limit: Maximum number of tags to retrieve.
    :param db: AsyncSession instance for database interaction.
    :param user: Current authenticated user.
    :return: List of TagResponse objects.
    """
    tags = await repository_tags.get_tags(skip, limit, db)
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
async def read_tag(tag_id: int, db: AsyncSession = Depends(get_db),
                   user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a specific tag by ID.

    :param tag_id: ID of the tag to retrieve.
    :param db: AsyncSession instance for database interaction.
    :param user: Current authenticated user.
    :return: TagResponse object.
    """
    tag = await repository_tags.get_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.post("/", response_model=TagResponse)
async def create_tag(body: TagModel, db: AsyncSession = Depends(get_db),
                     user: User = Depends(auth_service.get_current_user)):
    """
    Create a new tag.

    :param body: Data representing the new tag.
    :param db: AsyncSession instance for database interaction.
    :param user: Current authenticated user.
    :return: Newly created TagResponse object.
    """
    return await repository_tags.create_tag(body, db)


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(body: TagModel, tag_id: int, db: AsyncSession = Depends(get_db),
                     user: User = Depends(auth_service.get_current_user)):
    """
    Update an existing tag by ID.

    :param tag_id: ID of the tag to update.
    :param body: Data representing the updated tag information.
    :param db: AsyncSession instance for database interaction.
    :param user: Current authenticated user.
    :return: Updated TagResponse object.
    """
    tag = await repository_tags.update_tag(tag_id, body, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.delete("/{tag_id}", response_model=TagResponse)
async def remove_tag(tag_id: int, db: AsyncSession = Depends(get_db),
                     user: User = Depends(auth_service.get_current_user)):
    """
    Delete a tag by ID.

    :param tag_id: ID of the tag to delete.
    :param db: AsyncSession instance for database interaction.
    :param user: Current authenticated user.
    :return: Deleted TagResponse object.
    """
    tag = await repository_tags.remove_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag
