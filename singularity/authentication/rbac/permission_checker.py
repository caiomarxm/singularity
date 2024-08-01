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

        memberships = getattr(user, f"{level}_memberships", [])
        entity_membership: OrganizationMembership | SquadMembership | None = next(
            (
                membership
                for membership in memberships
                if getattr(membership, f"{level}_id") == entity_id
            ),
            None,
        )

        if not (entity_membership and entity_membership.role):
            return False

        user_role_permissions = {
            role_permission.permission.name
            for role_permission in entity_membership.role.role_permissions
        }
        return permission in user_role_permissions
