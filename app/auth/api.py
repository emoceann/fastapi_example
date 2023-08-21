from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.utils import create_access_token
from app.user import models
from app.auth.services import authentication_service, register_service
from app.auth.models import TokenData
from app.user.models import UserOut

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def reg_user(
        data: models.UserIn,
        reg_service: register_service.RegisterUser = Depends()
):
    await reg_service.register_user(data)


@router.post("/token", response_model=TokenData | dict)
async def auth_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: authentication_service.AuthUser = Depends()
):
    user = await auth_service.check_credentials(form_data)
    if not user:
        return {'error': 'invalid login or password'}
    return {'access_token': create_access_token(user.model_dump()), 'token_type': 'bearer'}
