from pydantic import BaseModel

from singularity.database.models.rbac import PermissionCreate


class UserPermissions(BaseModel):
    view_self: PermissionCreate = PermissionCreate(
        name="user.self.view", description="Can view details of self user"
    )
    update_self: PermissionCreate = PermissionCreate(
        name="user.self.update", description="Can update details of self user"
    )
    create_user: PermissionCreate = PermissionCreate(
        name="user.create", description="Can create or invite a new user"
    )
    update_user: PermissionCreate = PermissionCreate(
        name="user.create", description="Can update an existing user"
    )
    list_users: PermissionCreate = PermissionCreate(
        name="user.list",
        description="Can view all existing user within a level of permission",
    )
    view_user: PermissionCreate = PermissionCreate(
        name="user.detail",
        description="Can view details of an existing user within a level of permission",
    )
    delete_user: PermissionCreate = PermissionCreate(
        name="user.delete", description="Can delete an existing user"
    )


class SquadMembershipsPermissions(BaseModel):
    add_user_to_squad: PermissionCreate = PermissionCreate(
        name="squad.membership.create",
        description="Can add users to an organization",
    )
    remove_user_from_squad: PermissionCreate = PermissionCreate(
        name="squad.membership.delete",
        description="Can add users to an organization",
    )


class SquadPermissions(BaseModel):
    create_squad_in_organization: PermissionCreate = PermissionCreate(
        name="squad.create",
        description="Can create squads within the Organization",
    )
    update_squad_in_organization: PermissionCreate = PermissionCreate(
        name="squad.update",
        description="Can update squads within the Organization",
    )
    list_squads_in_organization: PermissionCreate = PermissionCreate(
        name="squad.list",
        description="Can update squads within the Organization",
    )
    detail_squad_in_organization: PermissionCreate = PermissionCreate(
        name="squad.detail",
        description="Can update squads within the Organization",
    )
    delete_squad_in_organization: PermissionCreate = PermissionCreate(
        name="squad.delete",
        description="Can delete squads within the Organization",
    )


class OrganizationMembershipPermissions(BaseModel):
    add_user_to_organization: PermissionCreate = PermissionCreate(
        name="organization.membership.create",
        description="Can add users to an organization",
    )
    remove_user_from_organization: PermissionCreate = PermissionCreate(
        name="organization.membership.delete",
        description="Can add users to an organization",
    )


class OrganizationPermissions(BaseModel):
    create_organization: PermissionCreate = PermissionCreate(
        name="organization.create", description="Can create new organizations"
    )
    delete_organization: PermissionCreate = PermissionCreate(
        name="organization.delete", description="Can delete organizations"
    )
    view_organization: PermissionCreate = PermissionCreate(
        name="organization.view",
        description="Can view details of it's own organization",
    )
    update_organization: PermissionCreate = PermissionCreate(
        name="organization.update",
        description="Can update details of it's own organization",
    )


class RoleEntityPermissions(BaseModel):
    create_custom_role: PermissionCreate = PermissionCreate(
        name="role.create", description="Can create new custom roles"
    )
    delete_custom_role: PermissionCreate = PermissionCreate(
        name="role.delete", description="Can delete custom roles"
    )
    list_roles: PermissionCreate = PermissionCreate(
        name="role.list",
        description="Can list roles",
    )
    view_role: PermissionCreate = PermissionCreate(
        name="role.view",
        description="Can view details of a role",
    )
    update_custom_role: PermissionCreate = PermissionCreate(
        name="role.update",
        description="Can update details of a custom role",
    )


class PermissionEntityPermissions(BaseModel):
    list_permissions: PermissionCreate = PermissionCreate(
        name="permission.list",
        description="Can list permissions",
    )
    view_permission: PermissionCreate = PermissionCreate(
        name="permission.view",
        description="Can view details of a permission",
    )


class PredefinedPermissions(BaseModel):
    roles: RoleEntityPermissions = RoleEntityPermissions()
    permissions: PermissionEntityPermissions = PermissionEntityPermissions()

    organization: OrganizationPermissions = OrganizationPermissions()
    organization_membership: OrganizationMembershipPermissions = (
        OrganizationMembershipPermissions()
    )

    squad: SquadPermissions = SquadPermissions()
    squad_membership: SquadMembershipsPermissions = SquadMembershipsPermissions()

    user: UserPermissions = UserPermissions()


PREDEFINED_PERMISSIONS = PredefinedPermissions()
