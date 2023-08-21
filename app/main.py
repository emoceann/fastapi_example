from fastapi import FastAPI
import uvicorn

from app.auth.api import router as auth_app
from app.user.api import router as user_app


def setup_app() -> FastAPI:
    app = FastAPI()
    app.include_router(auth_app)
    app.include_router(user_app)
    return app


if __name__ == "__main__":
    uvicorn.run(setup_app())
