"""
Define the `MongoLogger` class for logging HTTP requests and errors to MongoDB, with Prometheus metrics integration.

Classes
-------
MongoLogger : class
    Handles logging of HTTP requests and errors to MongoDB, and integrates with Prometheus for metrics collection.
"""

import copy
import time
import traceback
from datetime import UTC, datetime

from flask import Flask, g, jsonify, request
from flask_pymongo import PyMongo
from utils.console_logger import get_console_logger

mongo_log = get_console_logger('mongo_logger')


class MongoLogger:
    """
    Log HTTP requests and errors to MongoDB and integrate with Prometheus for metrics collection.

    Parameters
    ----------
    db_mongo : PyMongo
        The PyMongo instance used to log data to MongoDB.


    Methods
    -------
    init_app(app)
        Initialize the logging setup for a Flask application.
    """

    def __init__(self, db_mongo: PyMongo):
        """
        Initialize the MongoLogger with a MongoDB connection and Prometheus namespace.

        Parameters
        ----------
        db_mongo : PyMongo
            The PyMongo instance used to log data to MongoDB.
        """
        self.logs_mongo = db_mongo

    def init_app(self, app: Flask):
        """
        Set up logging for HTTP requests and errors in the Flask application and add a '/metrics' route to access Prometheus metrics.

        Parameters
        ----------
        app : Flask
            The Flask application instance to initialize logging for.
        """
        mongo_log.info('Initializing Mongo Logger')

        @app.errorhandler(Exception)
        def handle_exception(e):
            """
            Handle exceptions, log the error details to MongoDB, and return a JSON response.

            Parameters
            ----------
            e : Exception
                The exception that was raised.

            Returns
            -------
            response : Response
                A JSON response containing error details.
            """
            body = None
            content_type = request.headers.get('Content-Type')
            if content_type == 'application/json':
                body = request.get_json()
            username = request.cookies.get('username')
            id_user = request.cookies.get('id_user')
            error_info = {
                'timestamp': datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'level': 'ERROR',
                'event': type(e).__name__,
                'error_code': getattr(e, 'code', 500),
                'error_message': str(e),
                'id_user': id_user,
                'username': username,
                'body': body,
                'user_agent': request.headers.get('User-Agent'),
                'stack_trace': traceback.format_exc(),
            }

            mongo_log.error(error_info)
            self.logs_mongo.db.exception.insert_one(copy.deepcopy(error_info))
            return jsonify(error_info), getattr(e, 'code', 500)

        @app.before_request
        def start_timer():
            """Start a timer before processing a request to measure request duration."""
            if 'start' not in g:
                g.start = {}
            g.start[request.headers.get('X-Request-ID', 'Unknown')] = time.time()

        @app.after_request
        def log_request(response):
            """
            Log the request and response details to MongoDB after the request is processed.

            Parameters
            ----------
            response : Response
                The Flask response object.

            Returns
            -------
            response : Response
                The same response object, returned for further processing.
            """
            id_request = request.headers.get('X-Request-ID', 'Unknown')
            if 'start' in g and id_request:
                response_time = round((time.time() - g.start[id_request]) * 1000)
            else:
                response_time = 'unknown'
            content_type = request.headers.get('Content-Type')
            username = request.cookies.get('username')
            id_user = request.cookies.get('id_user')
            body = None
            if content_type == 'application/json':
                body = request.get_json()
            response_req = None
            if response is not None:
                response_req = response.get_json()
            log_entry = {
                'timestamp': datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'level': 'INFO',
                'event': 'HttpRequest',
                'method': request.method,
                'endpoint': request.path,
                'status_code': response.status_code,
                'response_time_ms': response_time,
                'body': str(body),
                'response': response_req,
                'username': username,
                'id_user': id_user,
                'user_agent': request.headers.get('User-Agent'),
                'origin': request.headers.get('Origin', 'Unknown'),
            }
            self.logs_mongo.db.request.insert_one(copy.deepcopy(log_entry))
            mongo_log.info(f'{request.method} {request.path} {response.status_code} {response_time}ms registered')
            mongo_log.debug(log_entry)
            return response
