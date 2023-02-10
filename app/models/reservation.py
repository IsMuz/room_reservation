from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey

# Импортируем базовый класс для моделей.
from app.core.db import Base


class Reservation(Base):
    # Имя переговорки должно быть не больше 100 символов,
    # уникальным и непустым.
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    meetingroom_id = Column(Integer, ForeignKey('meetingroom.id'))