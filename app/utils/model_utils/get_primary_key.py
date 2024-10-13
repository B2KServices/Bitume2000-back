from setup import db
from sqlalchemy import Column, inspect
from sqlalchemy.orm import Mapper


def get_primary_key(model: type[db.Model]) -> Column | None:
    """
    Retrieve the primary key column of a SQLAlchemy model.

    Parameters
    ----------
    model : type[db.Model]
        The SQLAlchemy model class for which to retrieve the primary key.

    Returns
    -------
    Column or None
        The primary key column of the model if found and matches the convention 'id*';
        otherwise, returns the first primary key column. Returns None if no primary key is found.

    Notes
    -----
    - This function assumes that 'db' is an instance of SQLAlchemy and is imported correctly.
    - It checks for a primary key column starting with 'id'. If none matches, it returns the first primary key column.
    - Modify the function according to specific primary key naming conventions or additional requirements.

    """
    mapper: Mapper = inspect(model)
    primary_key_candidates = [column for column in mapper.primary_key if column.name.startswith('id')]
    if len(primary_key_candidates) > 0:
        return primary_key_candidates[0]
    else:
        return mapper.primary_key[0]
