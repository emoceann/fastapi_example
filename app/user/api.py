from fastapi import APIRouter, Depends

from app.user.models import UserOut
from app.user.services.users_service import UsersHandler
from app.auth.services.authentication_service import get_current_user
from app.user import models

router = APIRouter(prefix="/users")


@router.get("/all", response_model=list[UserOut] | None)
async def user_all(
        service: UsersHandler = Depends(),
        user=Depends(get_current_user)
):
    return await service.user_all()


@router.get("/id/{user_id}", response_model=models.UserOut | None)
async def user_by_id(
        user_id: int,
        service: UsersHandler = Depends(),
        user=Depends(get_current_user)
):
    return await service.user_by_id(user_id)


@router.get("/name/{username}", response_model=models.UserOut | None)
async def user_by_name(
        username: str,
        service: UsersHandler = Depends(),
        user=Depends(get_current_user)
):
    return await service.user_by_name(username)


@router.delete("/delete/{user_id}", status_code=204)
async def delete_user(
        user_id: int,
        service: UsersHandler = Depends(),
        user=Depends(get_current_user)
):
    return await service.user_delete(user_id)


@router.put("/update/{user_id}", status_code=204)
async def update_user(
        user_id: int, data: models.UserUpdate,
        service: UsersHandler = Depends(),
        user=Depends(get_current_user)
):
    await service.user_update(user_id, data)
