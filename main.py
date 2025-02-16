from fastapi import FastAPI, Depends, HTTPException, status, Query
from flightstat_scraper import flightStatScraper
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from db import models
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
scraper = flightStatScraper()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()

@app.get("/api/v1/flights")
async def get_flight(
    airline_code: str = Query(..., description="Airline code"),
    airline_no: str = Query(..., description="Flight number"),
    date: str = Query(..., description="Flight date (YYYY-MM-DD)")
):
    """endpoint that searches for flight information"""
    item = scraper.scrapeData(airline_code, airline_no, date)

    if not item or item[0].get('flightNo') == '':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check typo or format in parameters. Date format is 'YYYY-MM-DD' and it only can search 3 days before and after from today.")
    return item

@app.post("/api/v1/flights", response_model=Dict[str, Any])
async def insert_flight(
    airline_code: str = Query(..., description="Airline code"),
    airline_no: str = Query(..., description="Flight number"),
    date: str = Query(..., description="Flight date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """endpoint that searches for flight information and insert into the DB"""
    item = scraper.scrapeData(airline_code, airline_no, date)
    
    if not item or item[0].get('flightNo') == '':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check typo or format in parameters. Date format is 'YYYY-MM-DD' and it only can search 3 days before and after from today.")

    new_data = models.Data(
        flightNo=item[0].get('flightNo'),
        flightAirline=item[0].get('flightAirline'),
        flightStatus=item[0].get('flightStatus'),
        flightStatusDesc=item[0].get('flightStatusDesc'),
        departureAirportCode=item[0].get('departureAirportCode'),
        departureAirportName=item[0].get('departureAirportName'),
        departureCity=item[0].get('departureCity'),
        departureTerminal=item[0].get('departureTerminal'),
        departureGate=item[0].get('departureGate'),
        departureDate=item[0].get('departureDate'),
        departureTimeScheduled=item[0].get('departureTimeScheduled'),
        departureTimeActual=item[0].get('departureTimeActual'),
        departureTimeZone=item[0].get('departureTimeZone'),
        arrivalAirportCode=item[0].get('arrivalAirportCode'),
        arrivalAirportName=item[0].get('arrivalAirportName'),
        arrivalCity=item[0].get('arrivalCity'),
        arrivalTerminal=item[0].get('arrivalTerminal'),
        arrivalGate=item[0].get('arrivalGate'),
        arrivalBaggage=item[0].get('arrivalBaggage'),
        arrivalDate=item[0].get('arrivalDate'),
        arrivalTimeScheduled=item[0].get('arrivalTimeScheduled'),
        arrivalTimeActual=item[0].get('arrivalTimeActual'),
        arrivalTimeZone=item[0].get('arrivalTimeZone')
    )
    
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    
    return {"status": "success", "data": item}