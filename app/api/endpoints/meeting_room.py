# app/api/meeting_room.py

from fastapi import APIRouter, HTTPException, Depends

# Вместо импортов 6 функций импортируйте объект meeting_room_crud.
from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
from app.schemas.reservation import ReservationDB
from app.api.validators import check_meeting_room_exists, check_name_duplicate

# Импортируем класс асинхронной сессии для аннотации параметра.
from sqlalchemy.ext.asyncio import AsyncSession

# Импортируем асинхронный генератор сессий.
from app.core.db import get_async_session
from app.models.meeting_room import MeetingRoom

router = APIRouter(
    # prefix='/meeting_rooms',
    # tags=['Meeting Rooms']
)


@router.post(
    '/',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True
)
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
    # Указываем зависимость, предоставляющую объект сессии, как параметр функции.
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(meeting_room.name, session)
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.get(
    '/',
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True
)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session)
):
    room_list = await meeting_room_crud.get_multi(session)
    return room_list


@router.patch(
    # ID обновляемого объекта будет передаваться path-параметром.
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def partially_update_meeting_room(
    # ID обновляемого объекта.
    meeting_room_id: int,
    # JSON-данные, отправленные пользователем.
    obj_in: MeetingRoomUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    # Получаем объект из БД по ID.
    # В ответ ожидается либо None, либо объект класса MeetingRoom.
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)

    if obj_in.name is not None:
        # Если в запросе получено поле name — проверяем его на уникальность.
        await check_name_duplicate(obj_in.name, session)

    # Передаём в корутину все необходимые для обновления данные.
    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def remove_meeting_room(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    # Выносим повторяющийся код в отдельную корутину.
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    meeting_room = await meeting_room_crud.remove(
        meeting_room, session
    )
    return meeting_room

@router.get(
    '/{meeting_room_id}/reservations',
    response_model=list[ReservationDB]
)
async def get_reservations(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await check_meeting_room_exists(
        meeting_room_id, session
    )
    reservations = await reservation_crud.get_future_reservations_by_meeting_room(
        meeting_room_id, session
    )
    return reservations
