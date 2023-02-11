from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

# Импортируем базовый класс для моделей.
from app.core.db import Base
from app.models.reservation import Reservation


class MeetingRoom(Base):
    # Имя переговорки должно быть не больше 100 символов,
    # уникальным и непустым.
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    reservations = relationship(Reservation, cascade='delete')
