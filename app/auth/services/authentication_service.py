from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import check_password
from app.db.config import get_session
from app.settings import get_settings
from app.logger import log
from app.user import models
from app.user.services import db_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
setting = get_settings()


class AuthUser:
    def __init__(self, db_session: AsyncSession = Depends(get_session)):
        self.session = db_session

    async def check_credentials(self, data: OAuth2PasswordRequestForm) -> models.UserOut | bool:
        user = await db_service.get_user_by_name(data.username, self.session)
        if not user:
            return False
        if not check_password(user.password, data.password):
            return False
        return models.UserOut(id=user.id, name=user.name)


async def get_current_user(token: str = Depends(oauth2_scheme), db_session: AsyncSession = Depends(get_session)):
    try:
        payload = jwt.decode(token, setting.JWT_SECRET_KEY, algorithms=[setting.JWT_ENCRYPT_ALGORITHM])
        user = await db_service.get_user_by_id(payload.get("id"), db_session)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
        return user
    except jwt.ExpiredSignatureError as e:
        log.exception(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Expired token')
    except Exception as e:
        log.exception(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
