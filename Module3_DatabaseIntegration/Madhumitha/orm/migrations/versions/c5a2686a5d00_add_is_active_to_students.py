"""add is_active to students

Revision ID: c5a2686a5d00
Revises: 0212acadfbf7
Create Date: 2026-07-17 13:57:18.826410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5a2686a5d00'
down_revision: Union[str, Sequence[str], None] = '0212acadfbf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('students', sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.true()))


def downgrade() -> None:
    op.drop_column('students', 'is_active')
