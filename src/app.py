from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app)


### Flights ###

@app.route("/flights", methods=['POST'])
async def list_flights():
    data_json = request.json
    date = data_json["date"]
    try:
        fecha = datetime.strptime(date, "%d/%m/%Y") # DD/MM/YYYY
        if fecha.date() >= datetime.now().date():
            flights_response = get_flights_response(data_json)
            return flights_response.content
        else:
            return jsonify({
        "error": "invalid date"
    }), 400
    except ValueError:
        return jsonify({
        "error": "invalid date format",
    }), 400
    

def get_flights_response(data_json):
    return requests.get(
        "http://latam_scraper:3000/flights", 
        headers = {'content-type': 'application/json'},
        json=data_json)


### Bus Trips ###

@app.route("/bus_trips", methods=['POST'])
async def list_bus_trips():
    data_json = request.json
    date = data_json["date"]
    try:
        fecha = datetime.strptime(date, "%d/%m/%Y") # DD/MM/YYYY
        if fecha.date() >= datetime.now().date():
            bus_trips_response = get_bus_trips_response(data_json)
            return bus_trips_response.content
        else:
            return jsonify({
        "error": "invalid date"
    }), 400
    except ValueError:
        return jsonify({
        "error": "invalid date format",
    }), 400
    

def get_bus_trips_response(data_json):
    return requests.get(
        "http://turbus_scraper:6000/bus_trips", 
        headers = {'content-type': 'application/json'},
        json=data_json)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
