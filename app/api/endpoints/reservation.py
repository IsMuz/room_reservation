# app/api/endpoints/reservation.py
from fastapi import APIRouter, Depends
from app.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationDB
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.validators import check_reservation_intersections, check_meeting_room_exists, check_reservation_before_edit
from app.crud.reservation import reservation_crud

from app.core.db import get_async_session

router = APIRouter()


@router.post(
    '/',
    response_model=ReservationDB,
)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_meeting_room_exists(
        reservation.meetingroom_id,
        session
    )
    await check_reservation_intersections(
        **reservation.dict(),
        session=session
    )
    new_reservation = await reservation_crud.create(
        reservation, session
    )
    return new_reservation


@router.get(
    '/',
    response_model=list[ReservationDB],
)
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session)
):
    reservations = await reservation_crud.get_multi(session)
    return reservations


@router.delete(
    '/{reservation_id}',
    response_model=ReservationDB,
    response_model_exclude_none=True,
)
async def remove_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    # Выносим повторяющийся код в отдельную корутину.
    reservation = await check_reservation_before_edit(
        reservation_id, session
    )
    reservation = await reservation_crud.remove(
        reservation, session
    )
    return reservation


@router.patch('/{reservation_id}', response_model=ReservationDB)
async def update_reservation(
    reservation_id: int,
    obj_in: ReservationUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    # Проверяем, что такой объект бронирования вообще существует.
    reservation = await check_reservation_before_edit(
        reservation_id, session
    )
    # Проверяем, что нет пересечений с другими бронированиями.
    await check_reservation_intersections(
        # Новое время бронирования, распакованное на ключевые аргументы.
        **obj_in.dict(),
        # id обновляемого объекта бронирования,
        reservation_id=reservation_id,
        # id переговорки.
        meetingroom_id=reservation.meetingroom_id,
        session=session
    )
    reservation = await reservation_crud.update(
        db_obj=reservation,
        # На обновление передаем объект класса ReservationUpdate, как и требуется.
        obj_in=obj_in,
        session=session,
    )
    return reservation
