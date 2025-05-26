from fastapi import FastAPI
from src.adapters.driving.api.routes.auth_router import router as router_auth
from src.adapters.driving.api.routes.user_router import router as router_user
from src.adapters.driving.api.routes.base import router as router_base
from src.core import settings

app = FastAPI(
    title="Tech Challenge",
    description="API para o desafio Pos",
    version="0.0.1",
    license_info={
        "name": "MIT",
    },
    debug=settings.DEBUG,
)

app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_base)