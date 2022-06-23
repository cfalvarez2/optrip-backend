from scraper import TripOptions
from turbus_scraper import TurbusDate, TurbusScraper


ORIGIN = "Santiago"
DESTINATION = "Concepción"

DEPARTURE_DAY = 28
DEPARTURE_MONTH = 6  # June
DEPARTURE_YEAR = 2022

RETURN_DAY = 29
RETURN_MONTH = 6  # June
RETURN_YEAR = 2022


if __name__ == "__main__":
    departure_date = TurbusDate(DEPARTURE_DAY, DEPARTURE_MONTH, DEPARTURE_YEAR)
    return_date = TurbusDate(RETURN_DAY, RETURN_MONTH, RETURN_YEAR)
    
    options = TripOptions(ORIGIN, DESTINATION, departure_date, return_date)

    turbus_scraper = TurbusScraper()
    trips = turbus_scraper.scrape(options)

    print()
    [print(trip) for trip in trips]
