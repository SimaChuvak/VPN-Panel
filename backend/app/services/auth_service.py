from datetime import UTC, datetime, timedelta

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash

from app.core.config import settings
from app.models.user import User
from app.repositories.user_repository import UserRepository

password_hash = PasswordHash.recommended()
ACCESS_TOKEN_LIFETIME = timedelta(minutes=30)


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def authenticate(self, username: str, password: str) -> User:
        user = await self._repository.get_by_username(username)
        if user is None or not user.is_active or not password_hash.verify(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return user

    @staticmethod
    def create_access_token(user: User) -> str:
        expires_at = datetime.now(UTC) + ACCESS_TOKEN_LIFETIME
        return jwt.encode(
            {"sub": str(user.id), "role": user.role, "exp": expires_at},
            settings.jwt_secret,
            algorithm="HS256",
        )
