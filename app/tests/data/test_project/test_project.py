from http import HTTPStatus

from flask import url_for


def test_create_project(client, project_data, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    response = client.post(url_for('projects_blueprint.create_project'), json=project_data, headers=headers)
    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()
    assert data['title'] == project_data['title']


def test_get_projects(client, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    response = client.get(url_for('projects_blueprint.get_projects'), headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert isinstance(data, list)  # Check that it returns a list


def test_get_project(client, create_project_in_db, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    response = client.get(url_for('projects_blueprint.get_project', id_project=create_project_in_db.id_project), headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data['title'] == create_project_in_db.title


def test_update_project(client, create_project_in_db, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    updated_data = {'title': 'Updated Title'}
    response = client.patch(
        url_for('projects_blueprint.update_project', id_project=create_project_in_db.id_project), json=updated_data, headers=headers
    )
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data['title'] == updated_data['title']


def test_delete_project(client, create_project_in_db, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    response = client.delete(url_for('projects_blueprint.delete_project', id_project=create_project_in_db.id_project), headers=headers)
    assert response.status_code == HTTPStatus.OK


def test_get_project_contacts(client, create_project_in_db, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    response = client.get(url_for('projects_blueprint.get_project_contacts', id_project=create_project_in_db.id_project), headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert isinstance(data, list)  # Check that it returns a list


def test_get_user_projects(client, create_project_in_db, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    response = client.get(url_for('projects_blueprint.get_user_projects', id_project=create_project_in_db.id_project), headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert isinstance(data, list)  # Check that it returns a list
