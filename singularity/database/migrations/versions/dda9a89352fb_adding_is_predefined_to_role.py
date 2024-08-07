"""adding is_predefined to role

Revision ID: dda9a89352fb
Revises: c2b50c41b3df
Create Date: 2024-07-30 08:52:49.400133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'dda9a89352fb'
down_revision: Union[str, None] = 'c2b50c41b3df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('role', sa.Column('is_predefined', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('role', 'is_predefined')
    # ### end Alembic commands ###
