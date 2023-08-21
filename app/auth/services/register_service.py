from fastapi import Depends, HTTPException
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from app.db.config import get_session
from app.logger import log
from app.user import models
from app.user.services import db_service


class RegisterUser:
    def __init__(self, db_session: AsyncSession = Depends(get_session)):
        self.session = db_session

    async def register_user(self, user: models.UserIn):
        if await db_service.check_user_exists(user.name, self.session):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username already exists",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            user.password = bcrypt.hash(user.password)
            return await db_service.insert_user(user, self.session)
        except Exception as e:
            log.exception(e, exc_info=True)
