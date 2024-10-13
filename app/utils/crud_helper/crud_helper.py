"""A simple and flexible utility for managing basic CRUD operations on SQLAlchemy models."""

from http import HTTPStatus
from typing import Any

from flask import Response
from flask_sqlalchemy.model import Model
from marshmallow.schema import SchemaMeta
from utils.model_utils import get_primary_key
from utils.registry import SQLAlchemyRegistry
from utils.request_default_responses import DefaultResponse


class CRUDHelper:
    """
    Utility class for basic CRUD (Create, Read, Update, Delete) operations on an SQLAlchemy data model.

    Attributes
    ----------
    schema : SchemaMeta
        Instance of Marshmallow Schema for single object serialization.
    schema_many : SchemaMeta
        Instance of Marshmallow Schema for multiple objects serialization.
    model : Model
        SQLAlchemy model instance.
    name : str
        Table name of the model.
    registry : SQLAlchemyRegistry
        Registry for handling session management and model queries.

    Parameters
    ----------
    model : Model
        SQLAlchemy model class.
    schema : SchemaMeta
        Marshmallow schema class for serialization.
    db : SQLAlchemy
        SQLAlchemy database instance.
    """

    def __init__(self, model: Model, schema: SchemaMeta):
        self.schema = schema()
        self.schema_many = schema(many=True)
        self.model = model
        self.name = self.model.__tablename__
        self.registry = SQLAlchemyRegistry(model)

    def handle_get(self, id_instance: Any) -> tuple[Any, HTTPStatus]:
        """
        Retrieve an entity by its ID.

        Parameters
        ----------
        id_instance : Any
            ID of the instance to retrieve.

        Returns
        -------
        Tuple[Any, HTTPStatus]
            Tuple containing the serialized data and HTTP status.
        """
        entity = self.registry.get_one_by_id_or_fail(id_instance)
        return self.schema.dump(entity), HTTPStatus.OK

    def handle_get_by_index_and_offset(self, index: int = 0, offset: int = 10) -> tuple[list[Any], HTTPStatus]:
        """
        Retrieve entities by pagination using index and offset.

        Parameters
        ----------
        index : int, optional
            Page index number.
        offset : int, optional
            Number of records per page.

        Returns
        -------
        Tuple[List[Any], HTTPStatus]
            Tuple containing the list of serialized data and HTTP status.
        """
        entities = self.registry.get_by_page_and_offset(index, offset)
        return self.schema_many.dump(entities), HTTPStatus.OK

    def handle_get_all(self) -> tuple[list[Any], HTTPStatus]:
        """
        Retrieve all entities.

        Returns
        -------
        Tuple[List[Any], HTTPStatus]
            Tuple containing the list of all serialized data and HTTP status.
        """
        entities = self.registry.get_all()
        return_value = self.schema_many.dump(entities)
        return return_value, HTTPStatus.OK

    def handle_delete(self, id_instance):
        """
        Delete an entity by its ID.

        Parameters
        ----------
        id_instance : Any
            ID of the instance to delete.

        Returns
        -------
        Tuple[DefaultResponseType, HTTPStatus]
            Success message and HTTP status.
        """
        self.registry.delete_one_by_id_or_fail(id_instance)
        return DefaultResponse.success(), HTTPStatus.OK

    def handle_delete_all(self, data) -> tuple[Response, HTTPStatus]:
        """
        Delete multiple entities based on a list of IDs.

        Parameters
        ----------
        data : list
            List of IDs of instances to delete.

        Returns
        -------
        Tuple[DefaultResponseType, HTTPStatus]
            Success message and HTTP status.
        """
        for element_id in data:
            self.registry.delete_one_by_id_or_fail(element_id)
        return DefaultResponse.success(), HTTPStatus.OK

    def handle_put(self, id_instance: Any, data: Any) -> tuple[Any, HTTPStatus]:
        """
        Update an entity completely by its ID.

        Parameters
        ----------
        id_instance : Any
            ID of the instance to update.
        data : Any
            Data for updating the instance.

        Returns
        -------
        Tuple[Any, HTTPStatus]
            Tuple containing the updated serialized data and HTTP status.
        """
        entity = self.registry.get_one_by_id(id_instance)
        self.schema.load(data, instance=entity, partial=False)
        self.registry.update_one(entity)
        return self.schema.dump(entity), HTTPStatus.OK

    def handle_patch(self, id_instance: Any, data: Any) -> tuple[Any, HTTPStatus]:
        """
        Update an entity partially by its ID.

        Parameters
        ----------
        id_instance : Any
            ID of the instance to partially update.
        data : Any
            Data for partial updating of the instance.

        Returns
        -------
        Tuple[Any, HTTPStatus]
            Tuple containing the updated serialized data and HTTP status.
        """
        entity = self.registry.get_one_by_id(id_instance)
        self.schema.load(data, instance=entity, partial=True)
        self.registry.update_one(entity)
        return self.schema.dump(entity), HTTPStatus.OK

    def handle_patch_all(self, id_name: Any, data: Any) -> tuple[list[Any], HTTPStatus]:
        """
        Update multiple entities partially based on a given ID name and data list.

        Parameters
        ----------
        id_name : Any
            Attribute name to identify the entity by.
        data : list
            List containing data for partial updates.

        Returns
        -------
        Tuple[List[Any], HTTPStatus]
            Tuple containing the list of updated serialized data and HTTP status.
        """
        entities = []
        for item in data:
            entity = self.registry.get_one_by_id(item.get(id_name))
            self.schema.load(item, instance=entity, partial=True)
            entity = self.registry.update_one(entity)
            entities.append(self.schema.dump(entity))
        return entities, HTTPStatus.OK

    def handle_post_all(self, data) -> tuple[list[Any], HTTPStatus]:
        """
        Create multiple entities from given data.

        Parameters
        ----------
        data : list
            List of data to create entities.

        Returns
        -------
        Tuple[List[Any], HTTPStatus]
            Tuple containing the list of created serialized data and HTTP status CREATED.
        """
        entities = self.schema_many.load(data)
        self.registry.create_many(entities)
        return self.schema_many.dump(entities), HTTPStatus.CREATED

    def handle_post(self, data: Any) -> tuple[Any, HTTPStatus]:
        """
        Create an entity from given data.

        Parameters
        ----------
        data : Any
            Data to create an entity.

        Returns
        -------
        Tuple[Any, HTTPStatus]
            Tuple containing the created serialized data and HTTP status CREATED.
        """
        entity = self.schema.load(data)
        self.registry.create_one(entity)
        return self.schema.dump(entity), HTTPStatus.CREATED

    def handle_upsert(self, data: Any) -> tuple[Any, HTTPStatus]:
        """
        Create or update an entity based on existence check via primary key.

        Parameters
        ----------
        data : Any
            Data to create or update the entity.

        Returns
        -------
        Tuple[Any, HTTPStatus]
            Tuple containing the upserted serialized data and HTTP status CREATED or OK.
        """
        # entity = self.schema.load(data)
        primary_key = get_primary_key(self.model).name
        existing_entity = (
            self.registry.get_one_by_id(data[primary_key]) if hasattr(data, primary_key) and data[primary_key] and primary_key else None
        )
        if existing_entity is None:
            return self.handle_post(data)
        else:
            return self.handle_patch(data[primary_key], data)

    def handle_upsert_many(self, data_list: list) -> tuple[list[Any], HTTPStatus]:
        """
        Perform upsert operations on a list of data.

        Parameters
        ----------
        data_list : list
            List containing data for upsert operations.

        Returns
        -------
        Tuple[List[Any], HTTPStatus]
            Tuple containing the list of upserted serialized data and HTTP status CREATED.
        """
        results = []
        for data in data_list:
            result = self.handle_upsert(data)
            results.append(result[0])
        return results, HTTPStatus.CREATED
