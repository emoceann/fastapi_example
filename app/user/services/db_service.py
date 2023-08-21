from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update, ScalarResult
from app.user import models
from app.user.dao import User
from app.logger import log


async def check_user_exists(name: str, db_session: AsyncSession) -> bool:
    try:
        stmt = select(select(User).where(User.name == name).exists())
        return await db_session.scalar(stmt)
    except Exception as e:
        log.exception(e, exc_info=True)


async def insert_user(data: models.UserIn, db_session: AsyncSession):
    try:
        stmt = select(User.id, User.name).from_statement(insert(User).values(data.model_dump()).returning(User.id, User.name))
        result = await db_session.execute(stmt)
        await db_session.commit()
        return result.first()
    except Exception as e:
        log.exception(e, exc_info=True)


async def get_user_by_name(name: str, db_session: AsyncSession) -> ScalarResult:
    try:
        stmt = select(User).where(User.name == name)
        return await db_session.scalar(stmt)
    except Exception as e:
        log.exception(e, exc_info=True)


async def get_user_by_id(user_id: int, db_session: AsyncSession):
    try:
        return await db_session.get(User, user_id)
    except Exception as e:
        log.exception(e, exc_info=True)


async def delete_user(user_id: int, db_session: AsyncSession) -> None:
    try:
        stmt = delete(User).where(User.id == user_id)
        await db_session.execute(stmt)
        await db_session.commit()
    except Exception as e:
        log.exception(e, exc_info=True)


async def get_all_user(db_session: AsyncSession):
    try:
        stmt = select(User)
        return await db_session.scalars(stmt)
    except Exception as e:
        log.exception(e, exc_info=True)


async def update_user_data(user_id: int, data: models.UserUpdate, db_session: AsyncSession) -> None:
    try:
        stmt = update(User).where(User.id == user_id).values(**data.model_dump())
        await db_session.execute(stmt)
        await db_session.commit()
    except Exception as e:
        log.exception(e, exc_info=True)
