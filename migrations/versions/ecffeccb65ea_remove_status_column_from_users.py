"""remove status column from users

Revision ID: ecffeccb65ea
Revises: 92c8b4600bbb
Create Date: 2025-11-04 12:25:24.226808

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecffeccb65ea'
down_revision: Union[str, Sequence[str], None] = '92c8b4600bbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('user_details', 'status')

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('user_details', sa.Column(
        'status', sa.String(length=1), nullable=True))

    pass
