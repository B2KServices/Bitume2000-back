import os
from http import HTTPStatus

import pytest
from data.companies.models import CompanyModel
from data.companies.schemas import CompanySchema
from data.projects.models import ProjectModel
from data.projects.schemas import ProjectSchema
from data.users.controllers.user_controller import user_registry
from data.users.models import UserModel
from data.users.schemas import UserSchema
from setup import create_app, db
from tests.test_utils import read_file_as_json
from utils.crud_helper.crud_helper import CRUDHelper
from utils.registry import SQLAlchemyRegistry


def get_jwt_token(client, username, password):
    response = client.post('/api/auth/login', json={'username': username, 'password': password})
    assert response.status_code == HTTPStatus.OK
    return response.get_json()['access_token']


@pytest.fixture
def company_data():
    return {
        'name': 'Test Company',
        'phone': '0101010101',
        'siret': '123456789',
        'tva': '123456789',
        'siege_social': '1 rue de la paix',
    }


@pytest.fixture
def project_data(create_company_in_db):
    return {
        'title': 'Test Title',
        'description': 'Test Description',
        'bon_de_commande': '12345',
        'id_company': create_company_in_db.id_company,
        'status': 'ACTIVE',
    }


@pytest.fixture
def create_project_in_db(app, project_data):
    with app.app_context():
        project_helper = CRUDHelper(ProjectModel, ProjectSchema)
        project_dict = project_helper.handle_post(project_data)[0]
        project_registry = SQLAlchemyRegistry(ProjectModel)
        project = project_registry.get_one_by_id_or_fail(project_dict['id_project'])
        return project


@pytest.fixture
def create_company_in_db(app, company_data):
    with app.app_context():
        company_helper = CRUDHelper(CompanyModel, CompanySchema)
        company_dict = company_helper.handle_post(company_data)[0]
        company_registry = SQLAlchemyRegistry(CompanyModel)
        company = company_registry.get_one_by_id_or_fail(company_dict['id_company'])
        return company


@pytest.fixture
def create_admin_user_in_db(app, admin_user_data):
    with app.app_context():
        user_helper = CRUDHelper(UserModel, UserSchema)
        user_dict = user_helper.handle_post(admin_user_data)[0]
        user = user_registry.get_one_by_id_or_fail(user_dict['id_user'])
        return user


@pytest.fixture
def get_admin_jwt_token(client, create_admin_user_in_db):
    user = create_admin_user_in_db
    token = get_jwt_token(client, user.username, 'password')
    return token


def delete_database_content():
    print('DELETING DATABASE CONTENT', flush=True)
    for table in db.metadata.sorted_tables:
        try:
            db.session.execute(table.delete())
        except Exception as e:
            print(f'Error deleting table {table}: {e}', flush=True)
            continue
    db.session.commit()


@pytest.fixture(scope='session')
def app():
    os.environ['ENV'] = 'local'
    app = create_app()
    app.config.update(
        {
            'TESTING': True,
        }
    )
    return app


@pytest.fixture(scope='session')
def client(app):
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            delete_database_content()
        yield client


@pytest.fixture(scope='function', autouse=True)
def wipe_database_after_each_test(app, client):
    yield
    with app.app_context():
        delete_database_content()


@pytest.fixture
def clean_user_table(app):
    yield
    with app.app_context():
        UserModel.query.delete()
        db.session.commit()


@pytest.fixture
def populate_table_from_json(client):
    def _populate_table_from_json(table: db.Model, json_path: str):
        data = read_file_as_json(json_path)
        if isinstance(data, list):
            for row in data:
                db.session.add(table(**row))
        else:
            db.session.add(table(**data))
        db.session.commit()
        db.session.flush()
        return data

    return _populate_table_from_json


@pytest.fixture
def create_user(app):
    with app.app_context():
        data = {
            'name': 'Guilheim',
            'lastname': 'Chataing',
            'phone': '0606060606',
            'mail': 'guilheimchataing@gmail.com',
            'label': 'developer',
            'username': 'gchatain',
            'password': 'password',
            'address': '1 rue de la paix',
        }
        user_helper = CRUDHelper(UserModel, UserSchema)
        user = user_helper.handle_post(data)[0]
        return user


@pytest.fixture
def new_user_data():
    return {
        'name': 'Test',
        'lastname': 'User',
        'phone': '0101010101',
        'mail': 'testuser@example.com',
        'label': 'developer',
        'username': 'testuser',
        'password': 'password',
        'address': '1 rue de la paix',
    }


@pytest.fixture
def admin_user_data():
    return {
        'name': 'Admin',
        'lastname': 'User',
        'phone': '0101010101',
        'mail': 'admin@example.cpm',
        'label': 'admin',
        'username': 'admin',
        'password': 'password',
        'address': '1 rue de la paix',
    }


@pytest.fixture
def create_user_in_db(app, new_user_data):
    with app.app_context():
        user_helper = CRUDHelper(UserModel, UserSchema)
        user_dict = user_helper.handle_post(new_user_data)[0]
        user_registry = SQLAlchemyRegistry(UserModel)
        user = user_registry.get_one_by_id_or_fail(user_dict['id_user'])
        return user
