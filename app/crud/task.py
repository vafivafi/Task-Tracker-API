from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import TasksOrm
from app.schemas.task import TaskSchema
from app.loger.log import logger
from fastapi import HTTPException, status

class Taskcrud:
    
    @staticmethod
    async def get_all_task(
        session: AsyncSession, 
        owner_id: int,
        limit: int, 
        offset: int
    ) -> list[TasksOrm]:
        try:
            stmt = (
                select(TasksOrm)
                .where(TasksOrm.owner_id == owner_id)
                .order_by(TasksOrm.id)
                .offset(offset)
                .limit(limit)
            )
            result = await session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Ошбка при поиске всех задач {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Не удалось получить список задач"
            )

    @staticmethod
    async def create_task(
        session: AsyncSession, 
        task: TaskSchema,
        owner_id: int
    ) -> TasksOrm:
        new_task = TasksOrm(
            title = task.title,
            description = task.description,
            owner_id = owner_id
        )

        session.add(new_task)

        try:
            await session.commit()
            await session.refresh(new_task)
            logger.info("Задача добавлена")
            return new_task
        except Exception as e:
            logger.error(f"Ошибка при записи задачи {e}")
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось создать задачу"
            )
    
    @staticmethod
    async def get_one_task(
        session: AsyncSession,
        id: int
    ) -> TasksOrm:
       
        stmt = (
            select(TasksOrm)
            .where(TasksOrm.id == id)
        )
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()

        if task is None:
            logger.warning("Задача не найдена")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Задача не найдена"
            )

        return task
    
    @staticmethod
    async def update_task(
        session: AsyncSession,
        task_in: TaskSchema,
        id: int,
        owner_id: int
    ) -> TasksOrm:

        stmt = (
            select(TasksOrm)
            .where(TasksOrm.id == id, TasksOrm.owner_id == owner_id)
            .order_by(TasksOrm.id)
        )
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()

        if task is None:
            logger.warning("Задача не найдена")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Задача не найдена"
            )
        try:
            task.title = task_in.title
            task.description = task_in.description

            await session.commit()
            await session.refresh(task)
            return task
        except Exception as e:
            logger.error("Ошибка при записи задачи")
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Ошибка при записи задачи"
            )

    @staticmethod
    async def delete_task(
        session: AsyncSession,
        id: int,
        owner_id: int
    ) -> None:
        stmt = (
            select(TasksOrm)
            .where(TasksOrm.id == id, TasksOrm.owner_id == owner_id)
            .order_by(TasksOrm.id)
        )
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()

        if task is None:
            logger.warning("Задача не найдена")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

        try:
            await session.delete(task)
            await session.commit()
        except Exception as e:
            logger.error(f"Ошибка при удалении задачи {e}")
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Ошибка при удалении задачи"
            )


