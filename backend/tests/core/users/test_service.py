"""Testing user service."""

from typing import AsyncGenerator, Optional
from uuid import UUID

import pytest
from pydantic import UUID5

from app.core.users.models import User
from app.core.users.repo import UsersRepo
from app.core.users.service import find_users, register_user, remove_user


def uuid(n: int) -> UUID5:
    """Build UUID5 from int.

    Args:
        n: value to build from.

    Returns:
        UUID5.
    """
    return UUID(int=n, version=5)


def gen_user(n: int) -> User:
    """Generate user from index.

    Args:
        n: index of user.

    Returns:
        Generated user.
    """
    return User(id=uuid(n), username='name{idx}'.format(idx=n))


class RepoStub(UsersRepo):
    """Test class based on list."""

    def __init__(self) -> None:
        """Class initialisation with creating list with users."""
        super().__init__()
        self.users = {
            uuid(i): gen_user(i)
            for i in range(10)
        }

    async def create_user(self, username: str) -> Optional[User]:
        """Add user in storage if it not exist.

        Args:
            username: User to put in storage.

        Returns:
            Created user or None if user with such username already exists.
        """
        new_user_id = uuid(len(self.users))

        list_names = [user.username for user in self.users.values()]
        if username not in list_names:
            new_user = User(id=new_user_id, username=username)
            self.users[new_user_id] = new_user

            return new_user
        return None

    async def update_user(self, user: User) -> Optional[User]:
        """Update user in storage it if it exists.

        Args:
            user: User to update.

        Returns:
            Updated user and None if it not exists.
        """
        list_ids = [user.id for user in self.users.values()]
        if user.id in list_ids:
            self.users[user.id].username = user.username
            return user
        return None

    async def get_users(self) -> list[User]:
        """Get users from storage.

        Returns:
            List of users.
        """
        return list(self.users.values())

    async def get_user(self, user_id: UUID5) -> Optional[User]:
        """Get user by id from storage.

        Args:
            user_id: User id.

        Returns:
            User if it exists in storage.
        """
        return self.users.get(user_id)

    async def delete_user(self, user_id: UUID5) -> Optional[User]:
        """Delete user by id.

        Args:
            user_id: User id to delete.

        Returns:
            Deleted model of user.
        """
        return self.users.pop(user_id, None)

    async def find_users_by_name(self, query: str) -> list[User]:
        """Find users by part of username.

        Args:
            query: Part of name to search by.

        Returns:
            List of found users.
        """
        return [
            user for user in self.users.values()
            if query.lower() in user.username.lower()
        ]

    async def close(self) -> None:
        """Close storage and clean resources."""


@pytest.fixture
async def repo() -> AsyncGenerator[RepoStub, None]:
    """Provide users storage stub.

    Yields:
        Users storage stub with pre-defined items.
    """
    repo_stub = RepoStub()
    yield repo_stub
    await repo_stub.close()


async def test_register_user(
    repo: UsersRepo,
) -> None:
    """Register new user.

    Args:
        repo: User storage.
    """
    existed_user_name = 'name1'
    registered_user = await register_user(
        existed_user_name,
        repo,
    )
    assert registered_user is None

    unexisted_user_name = 'some_name'
    registered_user = await register_user(
        unexisted_user_name,
        repo,
    )
    assert registered_user is not None

    assert await repo.get_user(registered_user.id) == registered_user


async def test_remove_user(
    repo: UsersRepo,
) -> None:
    """Remove user from strorage.

    Args:
        repo: User storage.
    """
    user_id = uuid(1)
    user_name = 'name_1'
    await register_user(
        user_name,
        repo,
    )

    removed_user = await remove_user(
        user_id,
        repo,
    )

    assert removed_user is not None

    removed_user = await remove_user(
        user_id,
        repo,
    )

    assert removed_user is None


async def test_find_users(
    repo: UsersRepo,
) -> None:
    """Find users by part of username.

    Search is case insensitive.


    Args:
        repo: User storage.
    """
    assert await find_users('name', repo)
    assert not await find_users('unknown', repo)
