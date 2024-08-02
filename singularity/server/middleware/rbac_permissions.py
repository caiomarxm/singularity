ROUTE_PERMISSION_MAPPING = {
    "rbac": {
        "roles": {
            "": {
                "level": "admin",
                "permissions": {
                    "GET": "rbac.roles.list",
                    "POST": "rbac.roles.create",
                },
            },
            "{role_id}": {
                "level": "admin",
                "permissions": {
                    "GET": "rbac.roles.detail",
                    "PUT": "rbac.roles.update",
                    "DELETE": "rbac.roles.delete",
                },
            },
        },
    },
    # Add more routes as needed
}
