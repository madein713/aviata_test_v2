import uuid

from sqlalchemy import (
    Boolean, Column, Date, DateTime, ForeignKey, String, func, Integer, Float
)
from sqlalchemy.orm import relationship

from airflow.database import Base
from airflow.fsm import TicketSearchFSM


class BaseModel(Base):
    __abstract__ = True

    id = Column(
        Integer, primary_key=True, autoincrement=True
    )


class UUIDMixin(BaseModel):
    __abstract__ = True

    uuid = Column(
        'Уникальный номер', String(36),
        default=str(uuid.uuid4()), index=True
    )


class TimeStampMixin(BaseModel):
    __abstract__ = True

    created_at = Column(
        'Дата и время создания', DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        'Дата и время обновления', DateTime(timezone=True),
        onupdate=func.now()
    )


class FlightProvider(UUIDMixin, TimeStampMixin):
    __tablename__ = 'flights_providers'
    __mapper_args__ = {"eager_defaults": True}

    name = Column('Наименование поставщика', String(255), unique=True)
    url = Column('Адрес поставщика', String(255), unique=True)


class FlightSearch(UUIDMixin, TimeStampMixin, TicketSearchFSM):
    __tablename__ = 'flights_requests'

    departure_at = Column('Дата отправки', Date)
    departure_airport = Column('Город отправления', String(255))
    currency_code = Column('Код валюты клиента', String(5))
    departure_back_at = Column('Дата отправки обратно', Date, nullable=True)
    departure_back_airport = Column(
        'Город отправления обратно', String(255), nullable=True
    )
    back = Column('Обратный билет', Boolean, default=False)

    flights = relationship(
        'FlightInfo',
        back_populates='flight_search',
        lazy='selectin'
    )


class FlightInfo(UUIDMixin):
    __tablename__ = 'flights_info'

    departure_at = Column(
        'Дата и время отправки', DateTime
    )
    arrival_at = Column(
        'Дата и время прибытия', DateTime
    )
    departure_airport = Column(
        'Код города отправки', String(5), index=True
    )
    arrival_airport = Column(
        'Код города прибытия', String(5)
    )

    price = Column('Цена билета', Float(2))
    currency = Column(String(50))

    flight_search_id = Column(
        'Уникальный номер результата запроса', Integer,
        ForeignKey('flights_requests.id'), nullable=True
    )

    flight_search = relationship(
        'FlightSearch', back_populates='flights', lazy='selectin'
    )
