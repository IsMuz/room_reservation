from typing import Optional

from pydantic import BaseModel, Field, validator


class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(max_length=100)


    @validator('name')
    def name_is_not_none(cls, v):
        if v is None:
            raise ValueError('can not be none')
        return v

class MeetingRoomUpdate(MeetingRoomBase):
    @validator('name')
    def name_is_not_none(cls, v):
        if v is None:
            raise ValueError('can not be none')
        return v
    pass


class MeetingRoomDB(MeetingRoomBase):
    id: int

    class Config:
        orm_mode = True
