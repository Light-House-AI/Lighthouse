"""
Contains the base class for all models.
"""

from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from stringcase import snakecase


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return snakecase(cls.__name__)
