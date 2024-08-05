import pytest

from singularity.server.middleware.rbac.rbac_middleware import RBACMiddleware


class MockRequest:
    def __init__(self, path: str, method: str):
        self.url = type("URL", (), {"path": path})
        self.method = method


def test_resolve_permission_static():
    request = MockRequest("/rbac/roles/", "GET")
    middleware = RBACMiddleware(None)
    required_permission, level, entity_id = middleware.resolve_permission(request)
    assert required_permission == "rbac.roles.list"
    assert level == "admin"
    assert entity_id is None


def test_resolve_permission_static_without_slash():
    request = MockRequest("/rbac/roles", "GET")
    middleware = RBACMiddleware(None)
    required_permission, level, entity_id = middleware.resolve_permission(request)
    assert required_permission == "rbac.roles.list"
    assert level == "admin"
    assert entity_id is None


def test_resolve_permission_dynamic():
    request = MockRequest("/rbac/roles/1", "PUT")
    middleware = RBACMiddleware(None)
    required_permission, level, entity_id = middleware.resolve_permission(request)
    assert required_permission == "rbac.roles.update"
    assert level == "admin"
    assert entity_id == "1"


def test_resolve_permission_not_found():
    request = MockRequest("/rbac/invalid/1", "GET")
    middleware = RBACMiddleware(None)
    with pytest.raises(Exception):
        middleware.resolve_permission(request)
