"""Interface for working with user storage."""

from typing import Optional, Protocol

from pydantic import UUID5

from app.core.users.models import User


class UsersRepo(Protocol):
    """Interface for working with user storage."""

    async def create_user(self, username: str) -> Optional[User]:
        """Add user in storage if it not exist.

        Args:
            username: User to put in storage.

        Returns:
            Created user or None if user with such username already exists.
        """

    async def update_user(self, user: User) -> Optional[User]:
        """Update user in storage it if it exists.

        Args:
            user: User to update.

        Returns:
            Updated user and None if it not exists.
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

        Returns:
            Deleted model of user.
        """

    async def find_users_by_name(self, query: str) -> list[User]:
        """Find users by part of username.

        Search is case insensitive.

        Args:
            query: Part of name to search by.

        Returns:
            List of found users.
        """

    async def close(self) -> None:
        """Close storage and clean resources."""
