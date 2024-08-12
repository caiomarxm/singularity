from singularity.database.bootstrap_db import bootstrap_permissions
from singularity.database.repositories.rbac.permission_repository import (
    list_permissions,
)
from singularity.authentication.rbac.predefined.permissions import (
    PREDEFINED_PERMISSIONS,
)


def test_bootstrap_permissions(session):
    bootstrap_permissions(session)
    bootstrapped_names = [
        perm.name for perm in list_permissions(session=session, limit=999)
    ]

    predefined_names = []
    for _, category_permissions in PREDEFINED_PERMISSIONS.__dict__.items():
        for _, permission in category_permissions.__dict__.items():
            predefined_names.append(permission.name)

    for name in predefined_names:
        assert name in bootstrapped_names
