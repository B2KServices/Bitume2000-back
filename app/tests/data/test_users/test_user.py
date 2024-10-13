from http import HTTPStatus

from data.projects.schemas import ProjectSchema
from data.users.models import UserProjectModel
from flask import url_for
from setup import db
from tests.data.conftest import get_jwt_token


def test_create_user(client, new_user_data, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    response = client.post(url_for('users_blueprint.create_user'), json=new_user_data, headers=headers)
    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()
    assert data['username'] == new_user_data['username']


def test_get_user(client, get_admin_jwt_token, create_user_in_db):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    user = create_user_in_db
    response = client.get(url_for('users_blueprint.get_user', id_user=user.id_user), headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data['username'] == user.username


def test_update_user(client, create_user_in_db, get_admin_jwt_token):
    user = create_user_in_db
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    updated_data = {'name': 'UpdatedName'}
    response = client.patch(url_for('users_blueprint.update_user', id_user=user.id_user), json=updated_data, headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data['name'] == updated_data['name']


def test_get_me(client, create_user_in_db):
    user = create_user_in_db
    token = get_jwt_token(client, user.username, 'password')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get(url_for('users_blueprint.get_me'), headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data['username'] == user.username


def test_update_me(client, create_user_in_db):
    user = create_user_in_db
    token = get_jwt_token(client, user.username, 'password')
    headers = {'Authorization': f'Bearer {token}'}
    updated_data = {'name': 'UpdatedName'}
    response = client.patch(url_for('users_blueprint.update_me'), json=updated_data, headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data['name'] == updated_data['name']


def test_get_user_projects(client, create_user_in_db, create_company_in_db):
    user = create_user_in_db
    token = get_jwt_token(client, user.username, 'password')
    headers = {'Authorization': f'Bearer {token}'}

    with client.application.app_context():
        project = ProjectSchema().load(
            {
                'title': 'Test Title',
                'description': 'Test Description',
                'bon_de_commande': '12345',
                'id_company': create_company_in_db.id_company,
                'status': 'ACTIVE',
            }
        )
        db.session.add(project)
        db.session.commit()

        user_project = UserProjectModel(id_user=user.id_user, id_project=project.id_project)
        db.session.add(user_project)
        db.session.commit()

    response = client.get(url_for('users_blueprint.get_user_projects', id_user=user.id_user), headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['project']['title'] == 'Test Title'


def test_get_users(client, create_user_in_db, get_admin_jwt_token):
    user = create_user_in_db
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    response = client.get(url_for('users_blueprint.get_users'), headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert any(u['username'] == user.username for u in data)
