"""
Contains the base class for all models.
"""

from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from stringcase import snakecase
from sqlalchemy import inspect


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return snakecase(cls.__name__)

    def to_dict(self):
        """
        Convert an SQLAlchemy model instance to a dictionary.
        """
        inspection = inspect(self)

        columns = [c_attr.key for c_attr in inspection.mapper.column_attrs]
        relationships = [
            r_attr.key for r_attr in inspection.mapper.relationships
        ]
        unloaded_relationships = inspection.unloaded

        data = {}

        for column in columns:
            data[column] = getattr(self, column)

        for relationship in relationships:
            if relationship in unloaded_relationships:
                continue

            attr = getattr(self, relationship)
            if isinstance(attr, list):
                data[relationship] = [item.to_dict() for item in attr]
            else:
                data[relationship] = attr.to_dict()

        return data
