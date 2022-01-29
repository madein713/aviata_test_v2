from datetime import date, datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class FlightSearchBase:
    departure_at: date
    departure_airport: str


@dataclass
class FlightSearchCreate(FlightSearchBase):
    departure_back_at: Optional[date]
    departure_back_airport: Optional[str]
    arrival_airport: Optional[str]
    back: Optional[bool]
    currency_code: str = 'KZT'
