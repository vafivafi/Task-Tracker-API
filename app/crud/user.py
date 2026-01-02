from secure_python_utils import PasswordService
from app.loger.log import logger

class Secure:
    try:
        def password_hash(self, password: str) -> str:
            hashed = PasswordService.hash(password)
            logger.info("Пароль успешно захеширован")
            return hashed
    except Exception as e:
        logger.error(f"Ошибка при хешировании пароля: {e}")
        return None

    def verify_password(self, stored_hash: str, password: str) -> bool:
        try:    
            if PasswordService.verify(stored_hash, password):
                logger.info("Пароль совпадает")
                return True
            else:
                logger.error("Пароль не совпадает")
                return False
        except Exception as e:
            logger.error(f"Ошибка при верификации пароля: {e}")
            return False

