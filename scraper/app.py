from flask import Flask, jsonify, request
from latam_scraper import LatamDate, LatamScraper
from scraper import TripOptions
import os


LATAM_SCRAPER = LatamScraper()

app = Flask(__name__)


@app.route('/flights', methods=['GET'])
def get_flights():

    data = request.json

    origin = data["origin"]
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