import sys
from http import HTTPStatus

from werkzeug.test import TestResponse


def print_response_if_not_2xx(response: TestResponse):
    if not HTTPStatus.OK <= response.status_code < HTTPStatus.MULTIPLE_CHOICES:
        print(response.get_json(silent=True), file=sys.stderr, flush=True)
