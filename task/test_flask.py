from datetime import datetime

import pytest


def test_get_hello(client) -> None:
    resp = client.get('/hello')
    assert resp.data.decode('utf-8') == 'Hello'


@pytest.mark.parametrize("route", ["/hello", "/clients",
                                   "/clients/1"])
def test_get_client_status_200(client, route) -> None:
    resp = client.get(route)
    assert resp.status_code == 200


def test_create_client(client):
    response = client.post('/clients', json={'name': 'Serega',
                                          'surname': 'Rex',
                                          'credit_card': '123134214',
                                          'car_number': '1243AD-1'})
    assert response.status_code == 201
    data = response.get_json()
    assert data == {'id': 3, # id может отличаться, так как база данных может быть не пуста, зависит от конфигурации приложения в conftest.py
                    'name': 'Serega',
                    'surname': 'Rex',
                    'credit_card': '123134214',
                    'car_number': '1243AD-1'}

def test_create_parking(client):
    resp = client.post('/parking', json={
                                        "address": "Soviet 91",
                                        "opened": 1,
                                        "count_places": 10,
                                        "count_available_places": 10})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data == {"id": 2,
                    "address": "Soviet 91",
                    "opened": 1,
                    "count_places": 10,
                    "count_available_places": 10}

@pytest.mark.parking
def test_client_parking_in(client):
    resp = client.post('/client_parking', json={"client_id": 2,
                                                 "parking_id": 1})
    assert resp.status_code == 201
    data = resp.get_json()
    time_now = datetime.now().strftime("%a, %d %b %Y %X GMT")
    assert data == {"id": 2,
                    "client_id": 2,
                    "parking_id": 1,
                    "time_in": time_now,
                    "time_out": None}


@pytest.mark.parking
def test_client_parking_out(client):
    resp = client.delete('/client_parking', json={"client_id": 1,
                                                  "parking_id": 1})
    assert resp.status_code == 200
    data = resp.get_json()
    time_in_resp = data['time_in']
    time_now = datetime.now().strftime("%a, %d %b %Y %X GMT")
    assert data == {"id": 1,
                    "client_id": 1,
                    "parking_id": 1,
                    "time_in": time_in_resp,
                    "time_out": time_now}