import pytest
from app_latam import app as latam_app


@pytest.fixture()
def app():
    app = latam_app
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


def test_get_flights(client):
    test_data = {
        "origin":"SCL",
        "destination":"CCP",
        "date":"26/06/2022"
    }

    response = client.get("/flights", json=test_data)
    assert response.status_code == 200
    assert isinstance(response.json["flights"], list)
    assert response.json["origin"] == "SCL"
    assert response.json["destination"] == "CCP"
    assert response.json["date"] == "26/06/2022"
