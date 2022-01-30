from datetime import date, datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class FlightSearchBase:
    departure_at: date
    departure_airport: str


@dataclass
class FlightSearchCreate(FlightSearchBase):
    departure_back_at: Optional[date] = None
    departure_back_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    back: Optional[bool] = False
    currency_code: str = 'KZT'
