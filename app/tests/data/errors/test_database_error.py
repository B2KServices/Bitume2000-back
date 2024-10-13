import pytest
from data.companies.models import CompanyModel
from errors import BaseCustomError
from errors.database_errors import EntityNotFoundError, MultipleResultsFoundError, UnknownColumnError


def test_entity_not_found_error():
    with pytest.raises(EntityNotFoundError) as exc_info:
        raise EntityNotFoundError(CompanyModel, id_company=1, name='Test Company')

    assert str(exc_info.value) == ("No element found on table 'company' with the following parameters: id_company=1, name=Test Company")
    assert isinstance(exc_info.value, BaseCustomError)


def test_multiple_results_found_error():
    with pytest.raises(MultipleResultsFoundError) as exc_info:
        raise MultipleResultsFoundError(CompanyModel, id_company=1, name='Test Company')

    assert str(exc_info.value) == (
        "Request for one and only one element on table 'company', "
        'but multiple results found with the following parameters: id_company=1, name=Test Company'
    )
    assert isinstance(exc_info.value, BaseCustomError)


def test_unknown_column_error():
    with pytest.raises(UnknownColumnError) as exc_info:
        raise UnknownColumnError(CompanyModel, 'unknown_column')

    assert str(exc_info.value) == "Column 'unknown_column' doesn't exist on table 'company'"
    assert isinstance(exc_info.value, BaseCustomError)
