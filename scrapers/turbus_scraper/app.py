from flask import Flask, jsonify, request
from turbus_scraper import TurbusDate, TurbusScraper
from scraper import TripOptions
import os


TURBUS_SCRAPER = TurbusScraper()

app = Flask(__name__)


@app.route('/bus_trips', methods=['GET'])
def get_bus_trips():

    data = request.json

    origin = data["origin"] # Nombre ciudad ej: Concepción
    destination = data["destination"]
    departure_date = data["departure_date"] # DD/MM/YYYY
    return_date = data.get("return_date", None)

    departure_day, departure_month, departure_year = departure_date.split("/")
    return_day, return_month, return_year = return_date.split("/")
    
    turbus_departure_date = TurbusDate(int(departure_day), int(departure_month), int(departure_year))
    turbus_return_date = TurbusDate(int(return_day), int(return_month), int(return_year))
    options = TripOptions(origin, destination, turbus_departure_date, turbus_return_date)

    bus_trips = TURBUS_SCRAPER.scrape(options)
    
    return jsonify({
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "return_date": return_date,
        "bus_trips": bus_trips,
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)