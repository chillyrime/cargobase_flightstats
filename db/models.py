from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

# define table
class Data(Base):
    __tablename__ = "flightstat"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    search_date = Column(DateTime(timezone=True), default=func.now())
    flightNo = Column(String(50), nullable=False)
    flightAirline = Column(String(50), nullable=True)
    flightStatus = Column(String(50), nullable=True)
    flightStatusDesc = Column(String(50), nullable=True)
    departureAirportCode = Column(String(50), nullable=True)
    departureAirportName = Column(String(50), nullable=True)
    departureCity = Column(String(50), nullable=True)
    departureTerminal = Column(String(50), nullable=True)
    departureGate = Column(String(50), nullable=True)
    departureDate = Column(String(50), nullable=True)
    departureTimeScheduled = Column(String(50), nullable=True)
    departureTimeActual = Column(String(50), nullable=True)
    departureTimeZone = Column(String(50), nullable=True)
    arrivalAirportCode = Column(String(50), nullable=True)
    arrivalAirportName = Column(String(50), nullable=True)
    arrivalCity = Column(String(50), nullable=True)
    arrivalTerminal = Column(String(50), nullable=True)
    arrivalGate = Column(String(50), nullable=True)
    arrivalBaggage = Column(String(50), nullable=True)
    arrivalDate = Column(String(50), nullable=True)
    arrivalTimeScheduled = Column(String(50), nullable=True)
    arrivalTimeActual = Column(String(50), nullable=True)
    arrivalTimeZone = Column(String(50), nullable=True)