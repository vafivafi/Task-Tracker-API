from pydantic import BaseModel, Field

class TaskSchema(BaseModel):
    title: str = Field(
        min_length = 3,
        max_length = 40, 
        description = "Имя задачи пользователя",
        examples = ["Приготовить ужин"]
    )
    description: str = Field(
        min_length = 1,
        max_length = 2048,
        description = "Описание задачи пользователя",
        examples = ["Омлет: яйца, любые овощи (перец/помидор/лук/брокколи), зелень, немного масла."]
    )