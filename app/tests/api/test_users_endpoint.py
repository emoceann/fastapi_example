import pytest
from httpx import AsyncClient
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import create_access_token
from app.tests.utils import generate_random_string
from app.user.models import UserIn, UserOut
from app.user.services import db_service


@pytest.fixture(scope="session")
async def random_user(db_session):
    data = UserIn(name=generate_random_string(10), password=generate_random_string(16))
    data.password = bcrypt.hash(data.password)
    user = await db_service.insert_user(data, db_session)
    return UserOut(id=user.id, name=user.name)


class TestUserEndpoint:
    @pytest.mark.parametrize("endpoints", ["all", "name/asdasd", "id/234"])
    async def test_unauthorized(self, async_client: AsyncClient, endpoints):
        resp = await async_client.get("/users/" + endpoints)
        assert resp.status_code == 401

    @pytest.mark.parametrize("endpoints", ["id", "name"])
    async def test_get_user_by_id_and_name(self, async_client: AsyncClient, db_session: AsyncSession,
                                           random_user: UserOut, endpoints):
        data = random_user.model_dump()
        resp = await async_client.get(url=f"/users/{endpoints}/{data[endpoints]}",
                                      headers={"Authorization": f"Bearer {create_access_token(data)}"})
        assert resp.status_code == 200
        assert resp.json() == random_user.model_dump()

    async def test_update_user(self, async_client: AsyncClient, random_user: UserOut):
        data = random_user.model_dump()
        json_update = {"name": "testnameforupdate"}
        resp = await async_client.put(url=f"/users/update/{data['id']}", json=json_update,
                                      headers={"Authorization": f"Bearer {create_access_token(data)}"})
        assert resp.status_code == 204

    async def test_delete_user(self, async_client: AsyncClient, random_user: UserOut):
        resp = await async_client.delete(url=f"/users/delete/{random_user.id}", headers={
            "Authorization": f"Bearer {create_access_token(random_user.model_dump())}"})
        assert resp.status_code == 204
