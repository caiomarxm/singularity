from pydantic import BaseModel

from singularity.database.models.rbac import Permission


class UserPermissions(BaseModel):
    view_self: Permission = Permission(
        name="user.self.view", description="Can view details of self user"
    )
    update_self: Permission = Permission(
        name="user.self.update", description="Can update details of self user"
    )


class SquadMembershipsLevelPermissions(BaseModel):
    pass


class SquadLevelPermissions(BaseModel):
    pass


class OrganizationMembershipLevelPermissions(BaseModel):
    pass


class OrganizationLevelPermissions(BaseModel):
    view_organization: Permission = Permission(
        name="organization.view",
        description="Can view details of it's own organization",
    )
    update_organization: Permission = Permission(
        name="organization.update",
        description="Can update details of it's own organization",
    )
    create_squad_in_organization: Permission = Permission(
        name="organization.squads.create",
        description="Can create squads within the Organization",
    )
    update_squad_in_organization: Permission = Permission(
        name="organization.squads.update",
        description="Can update squads within the Organization",
    )
    list_squads_in_organization: Permission = Permission(
        name="organization.squads.list",
        description="Can update squads within the Organization",
    )
    detail_squad_in_organization: Permission = Permission(
        name="organization.squads.detail",
        description="Can update squads within the Organization",
    )


class SuperadminLevelPermissions(BaseModel):
    create_organization: Permission = Permission(
        name="organization.create", description="Can create new organizations"
    )
    delete_organization: Permission = Permission(
        name="organization.delete", description="Can delete organizations"
    )
