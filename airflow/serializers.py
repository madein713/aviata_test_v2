from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class FlightInfoBase:
    departure_at: date
    arrival_at: date
    departure_code: str
    departure_fullname: str
    arrival_code: str
    arrival_fullname: str
    ticket_price: float
    ticket_currency: str
    provider_result_id: int


@dataclass
class FlightInfoCreate(FlightInfoBase):
    pass


@dataclass
class FlightInfo(FlightInfoBase):
    id: int
    uuid: str

    class Config:
        orm_mode = True


@dataclass
class FlightSearchBase:
    departure_at: date
    departure_airport: str


@dataclass
class FlightSearchCreate(FlightSearchBase):
    arrival_airport: Optional[str]
    departure_back_at: Optional[date]
    departure_back_airport: Optional[str]
    arrival_back_airport: Optional[str]
    back: bool = False
    currency_code: str = 'KZT'


@dataclass
class FlightSearch(FlightSearchBase):
    created_at: datetime
    updated_at: Optional[datetime]
    currency_code: str
    id: int
    uuid: str
