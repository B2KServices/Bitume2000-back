from collections.abc import Callable, Iterable
from typing import TypeVar

import sqlalchemy.exc
from errors.database_errors import (
    EntityNotFoundError,
    MultipleResultsFoundError,
    UnknownColumnError,
)
from setup import db
from sqlalchemy import String, inspect
from sqlalchemy.orm import Mapper
from utils.model_utils import get_primary_key
from utils.registry import RegistryABC

InstanceType = TypeVar('InstanceType', bound=db.Model)


class SQLAlchemyRegistry(RegistryABC[InstanceType]):
    """
    A registry class for interfacing with SQLAlchemy models.

    This class provides methods for CRUD operations (Create, Read, Update, Delete)
    and querying operations on a SQLAlchemy model.

    Attributes
    ----------
    model : Callable[..., InstanceType]
        The SQLAlchemy model class associated with this registry.
    name : str
        The name of the database table associated with the SQLAlchemy model.

    Notes
    -----
    - Uses SQLAlchemy's session (`db.session`) for database operations.
    """

    def __init__(self, model: Callable[..., InstanceType]):
        self.model = model
        self.name = self.model.__tablename__

    def _save_entity(self, entity: InstanceType) -> InstanceType:
        """
        Helper method to add an entity to the session and commit changes.

        Parameters
        ----------
        entity : InstanceType
            The entity instance to save.

        Returns
        -------
        InstanceType
            The saved entity.
        """
        db.session.add(entity)
        db.session.commit()
        return entity

    def create_one(self, entity: InstanceType) -> InstanceType:
        """
        Saves a new entity to the table.

        Parameters
        ----------
        entity : InstanceType
            The entity instance to save.

        Returns
        -------
        InstanceType
            The saved entity (through a call to _save_entity() method).
        """
        return self._save_entity(entity)

    def update_one(self, entity: InstanceType) -> InstanceType:
        """
        Updates an existing entity in the table.

        Parameters
        ----------
        entity : InstanceType
            The entity instance to save.

        Returns
        -------
        InstanceType
            The saved entity (through a call to _save_entity() method).
        """
        return self._save_entity(entity)

    def delete_one_or_fail(self, entity: InstanceType):
        """
        Deletes an entity from the table; raises an error if the entity does not exist.

        Parameters
        ----------
        entity : InstanceType
            The entity instance to save.
        """
        db.session.delete(entity)
        db.session.commit()

    def delete_one_by_id_or_fail(self, id_instance: str):
        """
        Deletes an entity from the table by its primary key; raises an error if the entity does not exist.

        Parameters
        ----------
        id_instance : str
            The primary key identifier of the entity to delete.
        """
        entity = self.get_one_by_id_or_fail(id_instance)
        db.session.delete(entity)
        db.session.commit()

    def get_one_by_id(self, id_instance: str) -> InstanceType | None:
        """
        Retrieves an entity from the table by its primary key.

        Parameters
        ----------
        id_instance : str
            The primary key identifier of the entity to retrieve.

        Returns
        -------
        InstanceType | None
            The retrieved entity instance, or None if not found.
        """
        return db.session.get(self.model, id_instance, with_for_update=True)

    def get_by_page_and_offset(self, page: int, offset: int) -> [InstanceType]:
        """
        Retrieves entities from the table paginated by `page` and `offset`.

        Parameters
        ----------
        page : int
            The page number for pagination (starting from 0).
        offset : int
            The number of entities per page.

        Returns
        -------
        list[InstanceType]
            A list of entities retrieved based on the pagination parameters.
        """
        return db.session.query(self.model).offset(page * offset).limit(offset).all()

    def get_one_by_id_or_fail(self, id_instance: str) -> InstanceType:
        """
        Retrieves an entity from the table by its primary key; raises an error if the entity does not exist.

        Parameters
        ----------
        id_instance : str
            The primary key identifier of the entity to retrieve.

        Returns
        -------
        InstanceType
            The retrieved entity instance.

        Raises
        ------
        EntityNotFoundError
            If the entity with the specified primary key does not exist.
        """
        result = self.get_one_by_id(id_instance)
        if result is None:
            primary_key = get_primary_key(self.model)
            raise EntityNotFoundError(self.model, **{primary_key.name: id_instance})
        return result

    def _get_matching_mapper_columns(self, column_names: Iterable[str]):
        """
        Retrieves SQLAlchemy column objects that match the specified column names.

        Parameters
        ----------
        column_names : Iterable[str]
            Iterable of column names to retrieve.

        Returns
        -------
        list[Column]
            List of SQLAlchemy column objects corresponding to the specified column names.

        Raises
        ------
        UnknownColumnError
            If any of the specified column names do not exist in the SQLAlchemy model.
        """
        inst: Mapper = inspect(self.model)
        columns = []
        for col_name in column_names:
            column = inst.columns.get(col_name)
            if column is None:
                raise UnknownColumnError(self.model, col_name)
            columns.append(column)
        return columns

    def get_all_where(self, **kwargs) -> list[InstanceType]:
        r"""
        Retrieves all entities from the table that match the provided criteria.

        Parameters
        ----------
        \**kwargs
            Key-value pairs representing column names and their corresponding values for filtering.

        Returns
        -------
        list[InstanceType]
            A list of entities that match the provided filter criteria.
        """
        filtered_kwargs = {key: value for key, value in kwargs.items() if value is not None}
        self._get_matching_mapper_columns(filtered_kwargs.keys())
        return db.session.query(self.model).filter_by(**filtered_kwargs).all()

    def get_all_where_like(self, **kwargs) -> list[InstanceType]:
        r"""
        Retrieves all entities from the database where the specified columns match the provided patterns.

        Parameters
        ----------
        \**kwargs
            Key-value pairs representing column names and their corresponding patterns for filtering.

        Returns
        -------
        list[InstanceType]
            A list of entities that match the provided pattern criteria.

        Raises
        ------
        UnknownColumnError
            If any of the specified column names do not exist in the SQLAlchemy model.

        Notes
        -----
        - Filters entities based on case-insensitive partial matching (`ilike`) for string columns.
        - Uses exact matching (`==`) for non-string columns.
        """
        filtered_kwargs = {key: value for key, value in kwargs.items() if value is not None}
        columns = self._get_matching_mapper_columns(filtered_kwargs.keys())
        string_columns = []
        other_columns = []
        for col in columns:
            if issubclass(type(col.type), String):
                string_columns.append(col)
            else:
                other_columns.append(col)
        string_column_conditions = [
            column.ilike(f'%{filtered_kwargs[col_name]}%')
            for (col_name, column) in zip(filtered_kwargs.keys(), string_columns, strict=False)
        ]
        other_columns_conditions = [
            col == filtered_kwargs[col_name] for (col_name, col) in zip(filtered_kwargs.keys(), other_columns, strict=False)
        ]
        return db.session.query(self.model).filter(*string_column_conditions, *other_columns_conditions).all()

    def get_one_or_fail_where(self, **kwargs) -> InstanceType:
        r"""
        Retrieves a single entity from the table that matches the provided criteria.

        Parameters
        ----------
        \**kwargs
            Key-value pairs representing column names and their corresponding values for filtering.

        Returns
        -------
        InstanceType
            The retrieved entity that matches the provided filter criteria.

        Raises
        ------
        EntityNotFoundError
            If no entity matches the provided filter criteria.
        MultipleResultsFoundError
            If multiple entities match the provided filter criteria.
        """
        try:
            result = db.session.query(self.model).filter_by(**kwargs).one_or_none()
            if result is None:
                raise EntityNotFoundError(self.model, **kwargs)
            return result
        except sqlalchemy.exc.MultipleResultsFound as err:
            raise MultipleResultsFoundError(self.model, **kwargs) from err

    def get_all(self):
        """
        Retrieves all entities from the table.

        Returns
        -------
        list[InstanceType]
            A list of all entities in the table.
        """
        return db.session.query(self.model).all()
