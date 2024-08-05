from sqlmodel import Session, select

from singularity.authentication.security.password_manager import PasswordManager
from singularity.authentication.rbac.predefined.permissions import (
    PREDEFINED_PERMISSIONS,
)

from singularity.database.repositories.rbac.user_repository import (
    create_user,
    read_user_from_email,
)
from singularity.settings.settings import settings
from singularity.database.models.rbac import UserCreate, Permission


def bootstrap_permissions(session: Session) -> None:
    # Collect all predefined permissions from the PREDEFINED_PERMISSIONS structure
    predefined_permissions = []
    for category_name, category_permissions in PREDEFINED_PERMISSIONS.__dict__.items():
        for permission_name, permission in category_permissions.__dict__.items():
            predefined_permissions.append(permission)

    # Extract permission names
    permission_names = [permission.name for permission in predefined_permissions]

    # Fetch existing permissions from the database
    existing_permissions = session.exec(
        select(Permission).where(Permission.name.in_(permission_names))
    ).all()

    existing_permission_names = {perm.name for perm in existing_permissions}

    # Filter out permissions that already exist
    permissions_to_create = [
        perm
        for perm in predefined_permissions
        if perm.name not in existing_permission_names
    ]
    # Add new permissions to the session and commit in a batch
    if permissions_to_create:
        session.add_all(permissions_to_create)
        session.commit()


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

    # Bootstrap predefined permissions and roles
    bootstrap_permissions(session=session)
