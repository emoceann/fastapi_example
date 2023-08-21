from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import get_session
from app.user.services import db_service
from app.user import models


class UsersHandler:
    def __init__(self, db_session: AsyncSession = Depends(get_session)):
        self.session = db_session

    async def user_by_id(self, user_id: int):
        result = await db_service.get_user_by_id(user_id, self.session)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return result

    async def user_by_name(self, name: str):
        result = await db_service.get_user_by_name(name, self.session)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return result

    async def user_all(self):
        return await db_service.get_all_user(self.session)

    async def user_delete(self, user_id: int):
        if not await db_service.get_user_by_id(user_id, self.session):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        await db_service.delete_user(user_id, self.session)

    async def user_update(self, user_id: int, data: models.UserUpdate):
        if not await db_service.get_user_by_id(user_id, self.session):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        await db_service.update_user_data(user_id, data, self.session)
