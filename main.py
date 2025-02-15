from fastapi import FastAPI
from flightstat_scraper import flightStatScraper

app = FastAPI()
scraper = flightStatScraper()

@app.get("/{airlineCode}/{airlineNo}/{departDate}")
async def read_item(airlineCode: str, airlineNo: str, departDate: str):
    item = scraper.scrapeData(airlineCode, airlineNo, departDate)

    if item[0].get('flightNo') != '':
        return item
    else:
        return "Check parameter. Date format is 'YYYY-MM-DD' and it only can search 3 days before and after from today."