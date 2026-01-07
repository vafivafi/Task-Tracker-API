from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    username : str = Field(
        min_length = 3,
        max_length = 20,
        pattern = r"^[a-zA-Z0-9_-]+$",
        description = "Уникальное имя пользователя",
        examples = ["Vadim_77"]
    )
    password : str = Field(
        min_length = 8,
        max_length = 64,
        description = "Пароль пользователя",
        examples=["SecretP@ss123"]
    )