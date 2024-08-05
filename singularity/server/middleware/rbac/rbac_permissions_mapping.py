from singularity.authentication.rbac.predefined.permissions import (
    PREDEFINED_PERMISSIONS,
)

RBAC_ROUTE_PERMISSION_MAPPING = {
    "rbac": {
        "roles": {
            "": {
                "level": "admin",
                "permissions": {
                    "GET": PREDEFINED_PERMISSIONS.roles.list_roles.name,
                    "POST": PREDEFINED_PERMISSIONS.roles.create_custom_role.name,
                },
            },
            "{role_id}": {
                "level": "admin",
                "permissions": {
                    "GET": PREDEFINED_PERMISSIONS.roles.view_role.name,
                    "PUT": PREDEFINED_PERMISSIONS.roles.update_custom_role.name,
                    "DELETE": PREDEFINED_PERMISSIONS.roles.delete_custom_role.name,
                },
            },
        },
    },
    # Add more routes as needed
}
