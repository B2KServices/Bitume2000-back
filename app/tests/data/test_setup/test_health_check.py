from http import HTTPStatus


def test_health_check_success(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json['message'] == 'Backend is up and database connection is successful.'
