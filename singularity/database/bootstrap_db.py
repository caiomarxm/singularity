from sqlmodel import Session, select
from typing import List

from singularity.authentication.security.password_manager import PasswordManager
from singularity.authentication.rbac.predefined.permissions import (
    PREDEFINED_PERMISSIONS,
)

from singularity.database.repositories.rbac.user_repository import (
    create_user,
    read_user_from_email,
)
from singularity.database.repositories.rbac.permission_repository import (
    create_permission,
)
from singularity.database.models.rbac import UserCreate, Permission

from singularity.settings.settings import settings


def bootstrap_permissions(session: Session) -> None:
    # Collect all predefined permissions from the PREDEFINED_PERMISSIONS structure
    predefined_permissions = []
    permission_names = []
    for category_name, category_permissions in PREDEFINED_PERMISSIONS.__dict__.items():
        for permission_name, permission in category_permissions.__dict__.items():
            predefined_permissions.append(permission)
            permission_names.append(permission_name)

    # Fetch existing permissions from the database
    existing_permissions = session.exec(
        select(Permission).where(Permission.name.in_(permission_names))
    ).all()

    existing_permission_names = {perm.name for perm in existing_permissions}

    # Filter out permissions that already exist
    permissions_to_create: List[Permission] = [
        perm
        for perm in predefined_permissions
        if perm.name not in existing_permission_names
    ]

    # Add new permissions to the session and commit in a batch
    if permissions_to_create:
        for permission in permissions_to_create:
            try:
                create_permission(session=session, permission_in=permission)
            except ValueError:
                pass


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
