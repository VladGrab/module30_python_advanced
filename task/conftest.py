import datetime

import pytest
from module_29_testing.hw.task.main import create_app, db as _db
from module_29_testing.hw.task.models import Client, Parking, Client_Parking


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        client = Client(id=1,
                    name="name",
                    surname="surname",
                    credit_card="2589765",
                    car_number="25878-BA9")
        client_2 = Client(id=2,
                    name="Vlad",
                    surname="Grab",
                    credit_card="55268789",
                    car_number="11148-BA6")
        parking = Parking(id=1,
                          address='Soviet 78',
                          opened=True,
                          count_places=10,
                          count_available_places=10)
        client_parking = Client_Parking(id=1,
                                        client_id=1,
                                        parking_id=1,
                                        time_in=datetime.datetime.now(),
                                        time_out=None)
        _db.session.add(client)
        _db.session.add(client_2)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client

@pytest.fixture
def db(app):
    with app.app_context():
        yield _db