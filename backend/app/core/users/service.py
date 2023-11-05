"""Methods for user manipulation."""
from typing import Optional

from pydantic import UUID5

from app.core.users.models import User
from app.core.users.repo import UsersRepo


async def register_user(
    username: str,
    repo: UsersRepo,
) -> Optional[User]:
    """Register new user.

    Args:
        username: User name.
        repo: User storage.

    Returns:
        Registered user model if it not exist yet.
    """
    return await repo.create_user(username)


async def remove_user(
    user_id: UUID5,
    repo: UsersRepo,
) -> Optional[User]:
    """Remove user from the storage by id.

    Args:
        user_id: id of removable user.
        repo: User storage.

    Returns:
        Removed user if it existed.
    """
    return await repo.delete_user(user_id)


async def get_user(
    user_id: UUID5,
    repo: UsersRepo,
) -> Optional[User]:
    """Get user from the storage by id.

    Args:
        user_id: id of user.
        repo: User storage.

    Returns:
        User if it exists.
    """
    return await repo.get_user(user_id)


async def find_users(
    query: str,
    repo: UsersRepo,
) -> list[User]:
    """Find users by part of username.

    Search is case insensitive.


    Args:
        query: Part of name to search by.
        repo: User storage.

    Returns:
        List of found users.
    """
    return await repo.find_users_by_name(query)
