from sqlmodel import Session

from singularity.authentication.security.password_manager import PasswordManager

from singularity.database.repositories.rbac.user_repository import (
    create_user,
    read_user_from_email,
)
from singularity.settings.settings import settings
from singularity.database.models.rbac import UserCreate


def init_db(session: Session) -> None:
    user = read_user_from_email(
        session=session, user_email=settings.FIRST_SUPERUSER_EMAIL
    )
    if not user:
        user_in = UserCreate(
            name=settings.FIRST_SUPERUSER_NAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=PasswordManager.hash_password(
                settings.FIRST_SUPERUSER_PASSWORD
            ),
            is_superadmin=True,
        )
        user = create_user(session=session, user_in=user_in)

    # TODO: Insert logic to populate with predefined permissions and roles
