from http import HTTPStatus

from flask import Blueprint
from managers.swagger_manager.doc_decorator import swagger
from marshmallow import fields
from setup import db, docs, bot
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from utils.request_default_responses import DefaultResponse

NAME = 'health_check'
health_check_blueprint = Blueprint(f'{NAME}_blueprint', __name__)


@swagger(
    responses={
        HTTPStatus.OK: {'description': 'Backend is up and database connection is successful', 'content': {'message': fields.String()}},
        500: {'description': 'Backend is up but database connection failed', 'content': {'message': fields.String()}},
    },
)
@health_check_blueprint.get('/')
async def do_health_check():
    """
    Perform a health check on the database connection.

    Attempts to execute a simple SQL query to check the database connection status.

    If successful, returns a response indicating the database is connected with status code HTTPStatus.OK.

    If an SQLAlchemyError occurs during the query execution, returns a response indicating
    the database is not connected with status code 500.

    Returns
    -------
    tuple
        A tuple containing a message indicating the database connection status
        and an HTTP status code.
    """
    await bot.send_message('test')
    try:
        db.session.execute(text('SELECT 1')).first()
        return DefaultResponse.success('Backend is up and database connection is successful.'), HTTPStatus.OK
    except SQLAlchemyError:
        return DefaultResponse.error('Backend is up but database connection failed.'), 500


docs.register_function(do_health_check, health_check_blueprint)
