from secure_python_utils import PasswordService
from app.loger.log import logger
from app.api.deps import SessionDep
from app.schemas.user import UserSchema
from app.models.user import UsersOrm
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import authx_service

class Secure:
    @staticmethod
    def password_hash(password: str) -> str:
        try:
            hashed = PasswordService.hash(password)
            logger.info("Пароль успешно захеширован")
            return hashed
        except Exception as e:
            logger.error(f"Ошибка при хешировании пароля: {e}")
            return None

    @staticmethod
    def verify_password(
        stored_hash: str, 
        password: str
    ) -> bool:
        try:    
            if PasswordService.verify(stored_hash, password):
                logger.info("Пароль совпадает")
                return True
            else:
                logger.error("Пароль не совпадает")
                return False
        except Exception as e:
            logger.warning(f"Ошибка при верификации пароля: {e}")
            return False

class Usercrud:
    @staticmethod
    async def register_user(
        session: AsyncSession, 
        user: UserSchema
    ):
        password_hashed = Secure.password_hash(user.password)
        if password_hashed is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Ошибка при обработке пароля"
            )
        new_user = UsersOrm(
            username = user.username,
            password = password_hashed,    
        )

        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            token = authx_service.create_access_token(uid=str(new_user.id))
            return {
                "Сообщение": "пользователь добавлен",
                "Имя пользователя": new_user.username,
                "Время создания": new_user.created_at,
                "access_token": token,
                "token_type": "bearer"
            }
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка при записи пользователя {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Пользователь с таким именем уже существует"
            )

    @staticmethod
    async def validation_user(session: AsyncSession, user: UserSchema):
        stmt = select(UsersOrm).where(UsersOrm.username == user.username)
        result = await session.execute(stmt)
        user_valid = result.scalar_one_or_none()

        if user_valid is None:
            logger.warning(f"Пользователь не найден")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Неверное имя пользователя или пароль"
            )

        if Secure.verify_password(user_valid.password, user.password):
            token = authx_service.create_access_token(uid=str(user_valid.id))
            logger.info(f"Пользователь {user.username} прошел валидацию")      
            return {
                "Сообщение": "Пользователь прошел валидацию", 
                "Пользователь": user_valid.username, 
                "access_token": token, 
                "token_type": "bearer"
            }
        else:
            logger.warning(f"Пользователь не найден")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Неверное имя пользователя или пароль"
            )



        
        




        

