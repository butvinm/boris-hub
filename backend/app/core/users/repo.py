"""Interface for working with user storage."""

from typing import Optional, Protocol

from pydantic import UUID5

from app.core.users.models import User


class UsersRepo(Protocol):
    """Interface for working with user storage."""

    async def put_user(self, user: User) -> User:
        """Update user in storage, add it if it not exist.

        Args:
            user: User to put in storage.

        Returns:
            Created user.
        """

    async def get_users(self) -> list[User]:
        """Get users from storage.

        Returns:
            List of users.
        """

    async def get_user(self, user_id: UUID5) -> Optional[User]:
        """Get user by id from storage.

        Args:
            user_id: User id.

        Returns:
            User if it exists in storage.
        """

    async def delete_user(self, user_id: UUID5) -> Optional[User]:
        """Delete user by id.

        Args:
            user_id: User id to delete.

        Return:
            Deleted model of user.
        """

    async def close(self) -> None:
        """Close storage and clean resources."""
