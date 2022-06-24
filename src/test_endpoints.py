import pytest
import json
from app import app as src_app


class ResponseMock:
    def __init__(self, content):
        self.content = content


@pytest.fixture()
def app():
    app = src_app
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


def test_get_bus_trips(mocker, client):
    mocker.patch(
        'app.get_bus_trips_response',
        return_value=ResponseMock({
            "bus_trips": [
                {"cost":16100,"departure_time":"06:25","duration":420},
                {"cost":23100,"departure_time":"06:25","duration":420},
                {"cost":14100,"departure_time":"07:10","duration":415}
            ],
            "origin":"Santiago",
            "destination":"Calama",
            "date":"26/06/2022"
        })
    )

    test_data = {
        "origin": "Santiago",
        "destination": "Calama",
        "date": "26/06/2022"
    }

    response = client.post("/bus_trips", json=test_data)

    assert response.status_code == 200
    assert response.json == {
        "bus_trips": [
            {"cost":16100,"departure_time":"06:25","duration":420},
            {"cost":23100,"departure_time":"06:25","duration":420},
            {"cost":14100,"departure_time":"07:10","duration":415}
        ],
        "origin":"Santiago",
        "destination":"Calama",
        "date":"26/06/2022"
    }


def test_get_flights(mocker, client):
    mocker.patch(
        'app.get_flights_response',
        return_value=ResponseMock({
            "flights": [
                {"cost":16100,"departure_time":"06:25","duration":420},
                {"cost":23100,"departure_time":"06:25","duration":420},
                {"cost":14100,"departure_time":"07:10","duration":415}
            ],
            "destination":"CCP",
            "origin":"SCL",
            "date":"26/06/2022"
        })
    )

    test_data = {
        "origin": "SCL",
        "destination": "CCP",
        "date": "26/06/2022"
    }

    response = client.post("/flights", json=test_data)
    assert response.status_code == 200
    assert response.json == {
        "flights": [
            {"cost":16100,"departure_time":"06:25","duration":420},
            {"cost":23100,"departure_time":"06:25","duration":420},
            {"cost":14100,"departure_time":"07:10","duration":415}
        ],
        "date": "26/06/2022",
        "destination":"CCP",
        "origin":"SCL",
    }
