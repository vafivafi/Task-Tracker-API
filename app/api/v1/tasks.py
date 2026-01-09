from fastapi import APIRouter, Depends, status, Query
from app.api.deps import SessionDep
from app.schemas.task import TaskSchema
from app.core.security import bearer_scheme, authx_service
from fastapi.security import HTTPAuthorizationCredentials
from authx import TokenPayload
from app.crud.task import Taskcrud

task_router = APIRouter(
    prefix = "/api/v1/tasks",
    tags = ["Tasks"]
)

@task_router.post(
    "/",
    summary = "Добавить задачу",
    status_code = status.HTTP_201_CREATED,  
)
async def add_tasks(
    session: SessionDep,
    new_task: TaskSchema,
    _: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    payload: TokenPayload = Depends(authx_service.access_token_required)
):
    task = await Taskcrud.create_task(
        session = session, 
        task = new_task, 
        owner_id = int(payload.sub)
    )

    return {
        "message": "Пользователь добавлен", 
        "задача": task
    }


@task_router.get(
    "/",
    summary = "Получить все задачи",
)
async def get_all_tasks(
    session: SessionDep,
    limit: int = Query(20, ge = 1, le = 100),
    offset: int = Query(0, ge = 0),
    _: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    payload: TokenPayload = Depends(authx_service.access_token_required)
):
    tasks = await Taskcrud.get_all_task(
        session = session, 
        limit = limit, 
        offset = offset,
        owner_id = int(payload.sub)
    )

    return {
        "message": "задачи выведены успешно", 
        "задачи": tasks
    }

@task_router.get(
    "/{id}",
    summary = "Найти задачу по айди",
)
async def get_one_tasks(
    session: SessionDep,
    id: int,
    _: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    payload: TokenPayload = Depends(authx_service.access_token_required)
):
    task = await Taskcrud.get_one_task(
        session = session, 
        id = id
    )

    return {
        "message": "Задача успешно найдена", 
        "задача": task
    }

@task_router.put(
    "/{id}",
    summary = "Обновить задачу по айди"
)
async def put_tasks(
    id: int,
    session: SessionDep,
    task_in: TaskSchema,
    _: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    payload: TokenPayload = Depends(authx_service.access_token_required)
):
    task = await Taskcrud.update_task(
        session = session, 
        owner_id = int(payload.sub), 
        id = id, 
        task_in = task_in
    )

    return {
        "message": "Задача успешно обновлена", 
        "задача": task
    }

@task_router.delete(
    "/{id}",
    summary = "Удалить задачу по айди"
)
async def delete_task(
    id: int,
    session: SessionDep,
    _: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    payload: TokenPayload = Depends(authx_service.access_token_required)
):
    await Taskcrud.delete_task(
        id = id,
        owner_id = int(payload.sub),
        session = session
    )
    return {
        "message": "задача удалена"
    }
