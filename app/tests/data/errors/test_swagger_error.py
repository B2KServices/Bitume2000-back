import pytest
from errors.swagger_errors.swagger_error import InvalidBodyContentTypeError, InvalidHeaderContentTypeError, InvalidResponseContentTypeError


def test_invalid_header_content_type_error():
    key = 'Content-Type'
    with pytest.raises(InvalidHeaderContentTypeError) as excinfo:
        raise InvalidHeaderContentTypeError(key)
    assert str(excinfo.value) == f'Invalid header content type for : {key} field'


def test_invalid_body_content_type_error_with_key():
    key = 'Payload'
    with pytest.raises(InvalidBodyContentTypeError) as excinfo:
        raise InvalidBodyContentTypeError(key)
    assert str(excinfo.value) == f'Invalid body content type for : {key} field'


def test_invalid_body_content_type_error_without_key():
    with pytest.raises(InvalidBodyContentTypeError) as excinfo:
        raise InvalidBodyContentTypeError()
    assert str(excinfo.value) == 'Invalid body content type'


def test_invalid_response_content_type_error():
    key = 'Accept'
    with pytest.raises(InvalidResponseContentTypeError) as excinfo:
        raise InvalidResponseContentTypeError(key)
    assert str(excinfo.value) == f'Invalid response content type for : {key} field'
