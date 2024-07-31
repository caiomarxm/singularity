from typing import Literal, Optional

from singularity.database.models.rbac import (
    User,
    OrganizationMembership,
    SquadMembership,
)


class PermissionChecker:
    @staticmethod
    def user_has_permission(
        user: User,
        permission: str,
        level: Literal["admin", "organization", "squad"],
        entity_id: Optional[int] = None,
    ) -> bool:
        """
        Checks if a user has a specific permission at a given level.

        Args:
            user: The user to check permissions for.
            permission: The permission to check.
            level: The level at which to check the permission (admin, organization, squad).
            entity_id: The ID of the entity (organization or squad) to check permissions for.

        Returns:
            True if the user has the permission at the specified level, False otherwise.
        """

        if user.is_superadmin:
            return True

        if level not in ["organization", "squad"]:
            raise ValueError("Invalid level")

        membership = f"{level}_memberships"
        field_id = f"{level}_id"

        entity_membership: OrganizationMembership | SquadMembership | None = next(
            filter(
                lambda x: getattr(x, field_id) == entity_id,
                getattr(user, membership),
            )
        )

        if not entity_membership:
            return False

        user_role = entity_membership.role

        if not user_role:
            return False

        return any(
            role_permission.permission.name == permission
            for role_permission in user_role.role_permissions
        )
