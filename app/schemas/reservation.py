from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator, root_validator


class Reservation(BaseModel):
    from_reserve: datetime
    to_reserve: datetime


class ReservationUpdate(Reservation):
    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, v):
        if v <= datetime.now():
            raise ValueError('can not be less now')
        return v

    @root_validator()
    def check_from_reserve_before_to_reserve(cls, vs):
        if vs['from_reserve'] >= vs['to_reserve']:
            raise ValueError('to can not be earlier than from')
        return vs

    pass


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


class ReservationDB(Reservation):
    id: int
    meetingroom_id: int

    class Config:
        orm_model = True
