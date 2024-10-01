from http import HTTPStatus

from flask import url_for


def test_create_company(client, company_data, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    response = client.post(url_for('companies_blueprint.create_company'), json=company_data, headers=headers)
    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()
    assert data['name'] == company_data['name']


def test_get_companies(client, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    response = client.get(url_for('companies_blueprint.get_companies'), headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert isinstance(data, list)  # Check that it returns a list


def test_get_company(client, create_company_in_db, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    response = client.get(url_for('companies_blueprint.get_company', id_company=create_company_in_db.id_company), headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data['name'] == create_company_in_db.name


def test_update_company(client, create_company_in_db, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    updated_data = {'name': 'Updated Company Name'}
    response = client.patch(
        url_for('companies_blueprint.update_company', id_company=create_company_in_db.id_company), json=updated_data, headers=headers
    )
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data['name'] == updated_data['name']


def test_get_company_projects(client, create_company_in_db, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    response = client.get(url_for('companies_blueprint.get_company_projects', id_company=create_company_in_db.id_company), headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert isinstance(data, list)  # Check that it returns a list


def test_get_company_contacts(client, create_company_in_db, get_admin_jwt_token):
    headers = {'Authorization': f'Bearer {get_admin_jwt_token}'}
    response = client.get(url_for('companies_blueprint.get_company_contacts', id_company=create_company_in_db.id_company), headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert isinstance(data, list)  # Check that it returns a list
