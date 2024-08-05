from pydantic import BaseModel

from singularity.database.models.rbac import Permission


class UserPermissions(BaseModel):
    view_self: Permission = Permission(
        name="user.self.view", description="Can view details of self user"
    )
    update_self: Permission = Permission(
        name="user.self.update", description="Can update details of self user"
    )
    create_user: Permission = Permission(
        name="user.create", description="Can create or invite a new user"
    )
    update_user: Permission = Permission(
        name="user.create", description="Can update an existing user"
    )
    list_users: Permission = Permission(
        name="user.list",
        description="Can view all existing user within a level of permission",
    )
    view_user: Permission = Permission(
        name="user.detail",
        description="Can view details of an existing user within a level of permission",
    )
    delete_user: Permission = Permission(
        name="user.delete", description="Can delete an existing user"
    )


class SquadMembershipsPermissions(BaseModel):
    add_user_to_squad: Permission = Permission(
        name="squad.membership.create",
        description="Can add users to an organization",
    )
    remove_user_from_squad: Permission = Permission(
        name="squad.membership.delete",
        description="Can add users to an organization",
    )


class SquadPermissions(BaseModel):
    create_squad_in_organization: Permission = Permission(
        name="squad.create",
        description="Can create squads within the Organization",
    )
    update_squad_in_organization: Permission = Permission(
        name="squad.update",
        description="Can update squads within the Organization",
    )
    list_squads_in_organization: Permission = Permission(
        name="squad.list",
        description="Can update squads within the Organization",
    )
    detail_squad_in_organization: Permission = Permission(
        name="squad.detail",
        description="Can update squads within the Organization",
    )
    delete_squad_in_organization: Permission = Permission(
        name="squad.delete",
        description="Can delete squads within the Organization",
    )


class OrganizationMembershipPermissions(BaseModel):
    add_user_to_organization: Permission = Permission(
        name="organization.membership.create",
        description="Can add users to an organization",
    )
    remove_user_from_organization: Permission = Permission(
        name="organization.membership.delete",
        description="Can add users to an organization",
    )


class OrganizationPermissions(BaseModel):
    create_organization: Permission = Permission(
        name="organization.create", description="Can create new organizations"
    )
    delete_organization: Permission = Permission(
        name="organization.delete", description="Can delete organizations"
    )
    view_organization: Permission = Permission(
        name="organization.view",
        description="Can view details of it's own organization",
    )
    update_organization: Permission = Permission(
        name="organization.update",
        description="Can update details of it's own organization",
    )


class RoleEntityPermissions(BaseModel):
    create_custom_role: Permission = Permission(
        name="role.create", description="Can create new custom roles"
    )
    delete_custom_role: Permission = Permission(
        name="role.delete", description="Can delete custom roles"
    )
    list_roles: Permission = Permission(
        name="role.list",
        description="Can list roles",
    )
    view_role: Permission = Permission(
        name="role.view",
        description="Can view details of a role",
    )
    update_custom_role: Permission = Permission(
        name="role.update",
        description="Can update details of a custom role",
    )


class PermissionEntityPermissions(BaseModel):
    list_permissions: Permission = Permission(
        name="permission.list",
        description="Can list permissions",
    )
    view_role: Permission = Permission(
        name="permission.view",
        description="Can view details of a permission",
    )


class PredefinedPermissions:
    roles = RoleEntityPermissions()
    permissions = PermissionEntityPermissions()

    organization = OrganizationPermissions()
    organization_membership = OrganizationMembershipPermissions()

    squad = SquadPermissions()
    squad_membership = SquadMembershipsPermissions()

    user = UserPermissions()


PREDEFINED_PERMISSIONS = PredefinedPermissions()
