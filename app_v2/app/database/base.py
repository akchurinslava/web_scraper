import re

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import Mapped, as_declarative, declared_attr, mapped_column


@as_declarative()
class Base:
    """Base class for all models."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    @declared_attr
    def __tablename__(self) -> str:
        """
        Return the table name.

        Returns:
        - str: The table name.
        """
        return "_".join(
            re.sub(
                "([A-Z][a-z]+)",
                r" \1",
                re.sub("([A-Z]+)", r" \1", self.__name__.replace("-", " ")),
            ).split()
        ).lower()
