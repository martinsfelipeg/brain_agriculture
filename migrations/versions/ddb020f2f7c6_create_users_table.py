"""create users table and farmers table

Revision ID: ddb020f2f7c6
Revises: 
Create Date: 2024-11-30 17:07:47.294638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddb020f2f7c6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'farmers',
        sa.Column('ndoc', sa.String, primary_key=True, unique=True, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('farm_name', sa.String, nullable=False),
        sa.Column('city', sa.String, nullable=False),
        sa.Column('state', sa.String, nullable=False),
        sa.Column('total_area', sa.Float, nullable=False),
        sa.Column('arable_area', sa.Float, nullable=False),
        sa.Column('vegetation_area', sa.Float, nullable=False),
        sa.Column('planted_crops', sa.String, nullable=False),
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, unique=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('email', sa.String, unique=True, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('farmers')
    op.drop_table('users')
