import logging
import sys
from http import HTTPStatus

import werkzeug
from config import config
from errors import BaseCustomError
from errors.authentication_errors import ForbiddenError, UnauthorizedError
from errors.database_errors import EntityNotFoundError
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from managers.app_error_handler import AppErrorHandlers
from managers.database_manager import DatabaseManager
from managers.requests_debugger import RequestsDebugger
from managers.swagger_manager import SwaggerInterface, SwaggerParams
from marshmallow import ValidationError
from utils.console_logger import setup_console_loggers_color

PARAMS = SwaggerParams(
    title='Genee Portail API',
    version='0.0.0',
    openapi_version='3.0.2',
    components={'securitySchemes': {'ApiKeyAuth': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}}},
    security_definitions={'ApiKeyAuth': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'}},
    security=[{'ApiKeyAuth': []}],
    info={
        'description': 'how to use the API with the authorization: \n'
        '1.	Enter your credentials: Provide your username and password in the authentication route below. \n'
        '2.	Retrieve the key: Upon successful authentication, you will receive an authentication key. \n'
        '3.	Authorize: Add the returned key by clicking on the “Authorize” button.'
    },
)
docs: SwaggerInterface = SwaggerInterface(PARAMS)
setup_console_loggers_color()
db_manager = DatabaseManager()
db = db_manager.add_postgres_database('DB')
jwt: JWTManager = JWTManager()


def create_app():
    """
    Factory function to create and configure a Flask application instance.

    This function initializes a Flask application, configures logging, error handling,
    database connections, Keycloak authentication, API documentation, request logging,
    and registers blueprints for various endpoints. Depending on the environment
    (dev, test, prod), different configurations and middleware are applied.

    Returns
    -------
    Flask
        The configured Flask application instance.

    Notes
    -----
    - This function assumes that configuration values are set in the `config` object.
    - It sets up logging to stream INFO-level messages to stdout.
    - Error handling is configured using `AppErrorHandlers`.
    - Database connections (PostgreSQL and MongoDB) are managed using `DatabaseManager`.
    - Keycloak authentication is set up using `KeycloakOpenID` and `KeycloakInterface`.
    - API documentation is handled by `FlaskApiSpec`.
    - CORS is enabled for all origins in non-production environments.
    - Request payload and response logging (`RequestsDebugger`) is enabled in development
      environments for debugging purposes.
    - In development environment (`dev`), database tables are created using `db.create_all()`.
    """
    app = Flask(__name__)
    app.config.from_object(config)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info(f'Using environment {config.ENV}')

    error_handler = AppErrorHandlers()
    error_handler.init_app(app)
    error_handler.register(BaseCustomError, HTTPStatus.BAD_REQUEST)
    error_handler.register(ValidationError, HTTPStatus.BAD_REQUEST)
    error_handler.register(UnauthorizedError, HTTPStatus.UNAUTHORIZED)
    error_handler.register(ForbiddenError, HTTPStatus.FORBIDDEN)
    error_handler.register(EntityNotFoundError, HTTPStatus.NOT_FOUND)
    error_handler.register(werkzeug.exceptions.NotFound, HTTPStatus.NOT_FOUND)
    error_handler.register(werkzeug.exceptions.MethodNotAllowed, HTTPStatus.METHOD_NOT_ALLOWED)
    error_handler.init_app(app)
    jwt.init_app(app)

    db_manager.init_app(app)

    from data.authentication.controllers import auth_blueprint
    from data.health_check.controllers import health_check_blueprint

    app.register_blueprint(health_check_blueprint, url_prefix='')
    app.register_blueprint(auth_blueprint, url_prefix='/api')

    docs.init_app(app)

    if config.ENV != 'deployed':
        payload_request_debugger = RequestsDebugger()
        payload_request_debugger.init_app(app)

    CORS(app, supports_credentials=True, resources={r'/*': {'origins': '*'}})

    if config.ENV == 'local':
        with app.app_context():
            db.create_all()


    return app
