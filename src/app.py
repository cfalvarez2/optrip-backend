from flask import Flask, request

import requests
import json


app = Flask(__name__)


### Flights ###

@app.route("/flights", methods=['POST'])
async def list_flights():
    data_json = request.json
    flights_response = get_flights_response(data_json)
    print(flights_response)
    return json.loads(flights_response.content.decode('latin-1'))

def get_flights_response(data_json):
    return requests.get(
        "http://latam_scraper:3000/flights", 
        headers = {'content-type': 'application/json'},
        data=json.dumps(data_json, ensure_ascii=False))


### Bus Trips ###

@app.route("/bus_trips", methods=['POST'])
async def list_bus_trips():
    data_json = request.json
    bus_trips_response = get_bus_trips_response(data_json)
    return json.loads(bus_trips_response.content.decode('latin-1'))

def get_bus_trips_response(data_json):
    return requests.get(
        "http://turbus_scraper:6000/bus_trips", 
        headers = {'content-type': 'application/json'},
        data=json.dumps(data_json, ensure_ascii=False))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)