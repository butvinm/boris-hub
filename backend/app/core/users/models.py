"""User models."""

from pydantic import UUID5, BaseModel


class User(BaseModel):
    """User representetion in business logic."""

    id: UUID5

    username: str
