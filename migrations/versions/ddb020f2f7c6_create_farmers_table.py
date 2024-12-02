"""create farmers table

Revision ID: ddb020f2f7c6
Revises: 13a61e39d2f6
Create Date: 2024-11-30 17:09:32.027472

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'ddb020f2f7c6'
down_revision: Union[str, None] = '13a61e39d2f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # No-op because farmers table was moved to the earlier migration
    pass


def downgrade() -> None:
    # No-op because farmers table was moved to the earlier migration
    pass
