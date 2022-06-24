from flask import Flask, jsonify, request
from scraper_turbus import TurbusDate, TurbusScraper
from utils_turbus import TripOptions


TURBUS_SCRAPER = TurbusScraper()

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

@app.route('/bus_trips', methods=['GET'])
def get_bus_trips():

    data = request.json

    origin = data["origin"]  # Nombre ciudad ej: Concepción
    destination = data["destination"]
    date = data["date"] # DD/MM/YYYY

    day, month, year = date.split("/")

    turbus_date = TurbusDate(int(day), int(month), int(year))
    options = TripOptions(origin, destination, turbus_date)

    bus_trips = TURBUS_SCRAPER.scrape(options)

    return jsonify({
        "origin": origin,
        "destination": destination,
        "date": date,
        "bus_trips": bus_trips,
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
