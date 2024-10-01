from http import HTTPStatus


def test_login(create_user, client, clean_user_table):
    response = client.post('api/auth/login', json={'username': 'gchatain', 'password': 'password'})
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json
