from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: Optional[str]
    email: str
    hashed_password: str
    is_superadmin: bool = False

    created_at: Optional[str] = Field(
        default=None, sa_column_kwargs={"default": "CURRENT_TIMESTAMP"}
    )
    updated_at: Optional[str] = Field(
        default=None,
        sa_column_kwargs={
            "default": "CURRENT_TIMESTAMP",
            "onupdate": "CURRENT_TIMESTAMP",
        },
    )

    # Relationships
    organization_memberships: List["OrganizationMembership"] = Relationship(
        back_populates="user"
    )
    squad_memberships: List["SquadMembership"] = Relationship(back_populates="user")


class UserCreate(SQLModel):
    name: Optional[str] = None
    email: str
    hashed_password: str
    is_superadmin: bool = False


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    hased_password: Optional[str] = None
    is_superadmin: Optional[bool] = None


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)
    description: Optional[str] = None

    # Relationships
    role_permissions: List["RolePermission"] = Relationship(back_populates="role")
    organization_memberships: List["OrganizationMembership"] = Relationship(
        back_populates="role"
    )
    squad_memberships: List["SquadMembership"] = Relationship(back_populates="role")


class RoleCreate(SQLModel):
    name: str
    description: Optional[str] = None


class RoleUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)
    description: Optional[str] = None

    # Relationships
    role_permissions: List["RolePermission"] = Relationship(back_populates="permission")


class PermissionCreate(SQLModel):
    name: str
    description: Optional[str] = None


class PermissionUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)
    created_at: Optional[str] = Field(
        default=None, sa_column_kwargs={"default": "CURRENT_TIMESTAMP"}
    )
    updated_at: Optional[str] = Field(
        default=None,
        sa_column_kwargs={
            "default": "CURRENT_TIMESTAMP",
            "onupdate": "CURRENT_TIMESTAMP",
        },
    )

    # Relationships
    squads: List["Squad"] = Relationship(back_populates="organization")
    organization_memberships: List["OrganizationMembership"] = Relationship(
        back_populates="organization"
    )


class OrganizationCreate(SQLModel):
    name: str


class OrganizationUpdate(SQLModel):
    name: Optional[str] = None


class Squad(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    organization_id: Optional[int] = Field(default=None, foreign_key="organization.id")

    # Relationships
    organization: Optional[Organization] = Relationship(back_populates="squads")
    squad_memberships: List["SquadMembership"] = Relationship(back_populates="squad")


class SquadCreate(SQLModel):
    name: str
    description: Optional[str] = None


class SquadUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class OrganizationMembership(SQLModel, table=True):
    __tablename__ = "organization_memberships"

    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    organization_id: int = Field(
        default=None, foreign_key="organization.id", primary_key=True
    )
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")

    # Relationships
    user: User = Relationship(back_populates="organization_memberships")
    organization: Organization = Relationship(back_populates="organization_memberships")
    role: Optional[Role] = Relationship(back_populates="organization_memberships")


class OrganizationMembershipCreate(SQLModel):
    user_id: int
    organization_id: int
    role_id: Optional[int] = None


class OrganizationMembershipUpdate(SQLModel):
    user_id: Optional[int] = None
    organization_id: Optional[int] = None
    role_id: Optional[int] = None


class SquadMembership(SQLModel, table=True):
    __tablename__ = "squad_memberships"

    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    squad_id: int = Field(default=None, foreign_key="squad.id", primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")

    # Relationships
    user: User = Relationship(back_populates="squad_memberships")
    squad: Squad = Relationship(back_populates="squad_memberships")
    role: Optional[Role] = Relationship(back_populates="squad_memberships")


class SquadMembershipCreate(SQLModel):
    user_id: int
    squad_id: int
    role_id: Optional[int] = None


class RolePermission(SQLModel, table=True):
    __tablename__ = "role_permissions"

    role_id: int = Field(default=None, foreign_key="role.id", primary_key=True)
    permission_id: int = Field(
        default=None, foreign_key="permission.id", primary_key=True
    )

    # Relationships
    role: Role = Relationship(back_populates="role_permissions")
    permission: Permission = Relationship(back_populates="role_permissions")
