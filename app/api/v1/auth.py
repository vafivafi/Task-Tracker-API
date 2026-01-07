from fastapi import APIRouter, status, Depends
from app.schemas.user import UserSchema
from app.api.deps import SessionDep
from app.crud.user import Usercrud
from app.core.security import authx_service


auth_router = APIRouter(
    prefix = "/api/v1/auth",
    tags = ["Authentication"]
)

@auth_router.post(
    "/register",
    status_code = status.HTTP_201_CREATED,
    summary = "Регистрация нового пользователя"
)
async def register(
    user_data: UserSchema,
    session: SessionDep
):

    return await Usercrud.register_user(session = session, user = user_data)

@auth_router.post(
    "/login",
    summary = "Вход в аккаунт"
)
async def login(
    user_data: UserSchema,
    session: SessionDep
):
    return await Usercrud.validation_user(session=session, user=user_data)