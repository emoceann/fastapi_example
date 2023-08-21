import pytest
import asyncio

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.main import setup_app
from app.user.dao import Base
from app.settings import get_settings

settings = get_settings()
test_db_url = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@localhost/{settings.TEST_DB}"


@pytest.fixture(scope="session", autouse=True)
def create_db():
    test_db_sync = test_db_url.replace("asyncpg", "psycopg2")
    if database_exists(test_db_sync):
        drop_database(test_db_sync)
    create_database(test_db_sync)
    yield
    drop_database(test_db_sync)


@pytest.fixture(scope="session", autouse=True)
async def create_engine(create_db):
    engine = create_async_engine(
        url=test_db_url,
        echo=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine


@pytest.fixture(scope="session")
async def db_session(create_engine):
    AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=create_engine)
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest.fixture(scope="session", autouse=True)
async def auto_rollback(db_session: AsyncSession):
    await db_session.rollback()


@pytest.fixture(scope="session")
async def app():
    return setup_app()


@pytest.fixture(scope="session")
async def async_client(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
