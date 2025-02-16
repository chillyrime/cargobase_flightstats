from fastapi import FastAPI, Depends
from flightstat_scraper import flightStatScraper
from sqlalchemy.orm import Session

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

@app.get("/{airlineCode}/{airlineNo}/{departDate}")
async def read_item(airlineCode: str, airlineNo: str, departDate: str, db:Session=Depends(get_db)):
    item = scraper.scrapeData(airlineCode, airlineNo, departDate)

    if item[0].get('flightNo') != '':
        new_data = models.Data(flightNo = item[0].get('flightNo'),
                               flightAirline = item[0].get('flightAirline'),
                               flightStatus = item[0].get('flightStatus'),
                               flightStatusDesc = item[0].get('flightStatusDesc'),
                               departureAirportCode = item[0].get('departureAirportCode'),
                               departureAirportName = item[0].get('departureAirportName'),
                               departureCity = item[0].get('departureCity'),
                               departureTerminal = item[0].get('departureTerminal'),
                               departureGate = item[0].get('departureGate'),
                               departureDate = item[0].get('departureDate'),
                               departureTimeScheduled = item[0].get('departureTimeScheduled'),
                               departureTimeActual = item[0].get('departureTimeActual'),
                               departureTimeZone = item[0].get('departureTimeZone'),
                               arrivalAirportCode = item[0].get('arrivalAirportCode'),
                               arrivalAirportName = item[0].get('arrivalAirportName'),
                               arrivalCity = item[0].get('arrivalCity'),
                               arrivalTerminal = item[0].get('arrivalTerminal'),
                               arrivalGate = item[0].get('arrivalGate'),
                               arrivalBaggage = item[0].get('arrivalBaggage'),
                               arrivalDate = item[0].get('arrivalDate'),
                               arrivalTimeScheduled = item[0].get('arrivalTimeScheduled'),
                               arrivalTimeActual = item[0].get('arrivalTimeActual'),
                               arrivalTimeZone = item[0].get('arrivalTimeZone')
                               )
        db.add(new_data)
        db.commit()
        db.refresh(new_data)

        return item
    else:
        return "Check parameter. Date format is 'YYYY-MM-DD' and it only can search 3 days before and after from today."