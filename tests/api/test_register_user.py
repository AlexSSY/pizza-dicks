from httpx import ASGITransport, AsyncClient

from main import app

client = TestClient(app)


def test_register_traffic_controller():
    response = client.post(
        '/users',
        json={
            'email': 'robert@mail.com',
            'password': 'password123'
        }
    )

    assert response.status_code == 201


def setup():
    pass


def teardown():
    pass