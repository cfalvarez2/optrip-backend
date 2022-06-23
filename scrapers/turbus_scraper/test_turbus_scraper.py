import pytest

from app import app as turbus_app


@pytest.fixture()
def app():
    app = turbus_app
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_get_bus_trips(client):
    test_data = {
        "origin": "Santiago",
        "destination": "Concepción",
        "departure_date": "23/06/2022",
        "return_date": "26/06/2022"
    }
    response = client.get("/bus_trips", json=test_data)
    assert response.status_code == 200
    assert isinstance(response.json["bus_trips"], list)
    assert response.json["origin"] == "Santiago"
    assert response.json["destination"] == "Concepción"
    assert response.json["departure_date"] == "23/06/2022"
    assert response.json["return_date"] == "26/06/2022"
