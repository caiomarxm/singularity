from sqlmodel import Session

from singularity.authentication.security.password_manager import PasswordManager
from singularity.authentication.rbac.predefined.permissions import (
    PREDEFINED_PERMISSIONS,
)

from singularity.database.repositories.rbac.user_repository import (
    create_user,
    read_user_from_email,
)
from singularity.database.repositories.rbac.permission_repository import (
    create_permissions_batch,
)
from singularity.database.models.rbac import UserCreate

from singularity.settings.settings import settings


def bootstrap_permissions(session: Session) -> None:
    predefined_permissions = []
    for category_name, category_permissions in PREDEFINED_PERMISSIONS.__dict__.items():
        for permission_name, permission in category_permissions.__dict__.items():
            predefined_permissions.append(permission)

    create_permissions_batch(session=session, permissions=predefined_permissions)


def bootstrap_db_defaults(session: Session) -> None:
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

    # Bootstrap predefined permissions and roles
    bootstrap_permissions(session=session)
