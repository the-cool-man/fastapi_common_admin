"""create admin_users table

Revision ID: 546f9fbd9cb7
Revises: 74ff37d8ddd6
Create Date: 2025-10-30 11:28:23.196263
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# ✅ Import your model
from src.models.user_model import AdminUser  # Use exact model file
# No need to import Base here

# Revision identifiers
revision: str = '546f9fbd9cb7'
down_revision: Union[str, Sequence[str], None] = '74ff37d8ddd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Run upgrade: create admin_users table."""
    bind = op.get_bind()
    AdminUser.__table__.create(bind, checkfirst=True)


def downgrade() -> None:
    """Run downgrade: drop admin_users table."""
    bind = op.get_bind()
    AdminUser.__table__.drop(bind, checkfirst=True)  # ✅ safer with checkfirst
