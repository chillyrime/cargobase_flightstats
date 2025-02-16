import logging
from lxml import html
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class flightStatScraper():

    def scrapeData(self, airlineCode, airlineNo, departDate):
        year = departDate.split("-")[0]
        month = departDate.split("-")[1]
        day = departDate.split("-")[2]

        url = f'https://www.flightstats.com/v2/flight-tracker/{airlineCode}/{airlineNo}?year={year}&month={month}&date={day}'

        # Request the page
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("request failed: %s", e)
            return [{"flightNo": ""}]

        # Parsing the page
        try:
            flightStat = html.fromstring(response.content)
        except Exception as e:
            logger.error("HTML parse failed: %s", e)
            return [{"flightNo": ""}]
        
        # Get elements (flight info)
        flightNo = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div[1]/div[1]/text()'))
        flightAirline = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div[1]/div[2]/text()'))
        flightStatus = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[1]/text()'))
        flightStatusDesc = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[2]/text()'))
        
        # Get elements (departure info)
        departureAirportCode = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/a/text()'))
        departureAirportName = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[3]/text()'))
        departureCity = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/text()'))
        departureTerminal = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[4]/div[1]/div[2]/text()'))
        departureGate = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[4]/div[2]/div[2]/text()'))
        departureDate = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/text()'))
        departureTimeScheduled = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/text()'))
        departureTimeActual = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[3]/div[2]/div[2]/text()'))
        departureTimeZone = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/span/text()')).strip()
        
        # Get elements (darrival info)
        arrivalAirportCode = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div[2]/div/div[3]/div/div[1]/a/text()'))
        arrivalAirportName = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[3]/text()'))
        arrivalCity = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/text()'))
        arrivalTerminal = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[4]/div[1]/div[2]/text()'))
        arrivalGate = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[4]/div[2]/div[2]/text()'))
        arrivalBaggage = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[4]/div[3]/div[2]/text()'))
        arrivalDate = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/text()'))
        arrivalTimeScheduled = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[3]/div[1]/div[2]/text()'))
        arrivalTimeActual = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[3]/div[2]/div[2]/text()'))
        arrivalTimeZone = ''.join(flightStat.xpath('//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[3]/div[2]/div[2]/span/text()')).strip()

        # put the result into the list
        infoList = []
        infoList.append({
            "flightNo" : flightNo,
            "flightAirline" : flightAirline,
            "flightStatus" : flightStatus,
            "flightStatusDesc" : flightStatusDesc,
            "departureAirportCode" : departureAirportCode,
            "departureAirportName" : departureAirportName,
            "departureCity" : departureCity,
            "departureTerminal" : departureTerminal,
            "departureGate" : departureGate,
            "departureDate" : departureDate,
            "departureTimeScheduled" : departureTimeScheduled,
            "departureTimeActual" : departureTimeActual,
            "departureTimeZone" : departureTimeZone,
            "arrivalAirportCode" : arrivalAirportCode,
            "arrivalAirportName" : arrivalAirportName,
            "arrivalCity" : arrivalCity,
            "arrivalTerminal" : arrivalTerminal,
            "arrivalGate" : arrivalGate,
            "arrivalBaggage" : arrivalBaggage,
            "arrivalDate" : arrivalDate,
            "arrivalTimeScheduled" : arrivalTimeScheduled,
            "arrivalTimeActual" : arrivalTimeActual,
            "arrivalTimeZone" : arrivalTimeZone,
        })
        
        logger.info("__scrapped data__: %s", infoList)
        return infoList