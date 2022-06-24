from flask import Flask, jsonify, request

from scraper_latam import LatamDate, LatamScraper
from utils_latam import TripOptions


LATAM_SCRAPER = LatamScraper()

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

@app.route('/flights', methods=['GET'])
def get_flights():

    data = request.json

    origin = data["origin"]  # Código IATA ej: SCL
    destination = data["destination"]
    date = data["date"] # DD/MM/YYYY

    day, month, year = date.split("/")
    
    latam_date = LatamDate(int(day), int(month), int(year))
    options = TripOptions(origin, destination, latam_date)

    flights = LATAM_SCRAPER.scrape(options)
    
    return jsonify({
        "origin": origin, 
        "destination": destination, 
        "date": date, 
        "flights": flights
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)