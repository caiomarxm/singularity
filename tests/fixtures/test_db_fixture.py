from sqlalchemy import inspect


def test_db_tables(session):
    # Use the inspector to get a list of table names
    inspector = inspect(session.get_bind())
    tables = inspector.get_table_names()

    expected_tables = [
        "user",
        "role",
        "permission",
        "organization",
        "squad",
        "organization_memberships",
        "squad_memberships",
        "role_permissions",
    ]
    assert set(expected_tables).issubset(set(tables))
