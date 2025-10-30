"""create admin_role

Revision ID: 74ff37d8ddd6
Revises: None
Create Date: 2025-10-30 11:38:17.434322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from src.models.admin_role_model import AdminRole



# revision identifiers, used by Alembic.
revision: str = '74ff37d8ddd6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    AdminRole.__table__.create(op.get_bind(), checkfirst=True)

    pass


def downgrade() -> None:
    """Downgrade schema."""

    AdminRole.__table__.drop(op.get_bind(), checkfirst=True)

    pass
