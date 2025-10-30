"""create site_config

Revision ID: 1090551e7519
Revises: 546f9fbd9cb7
Create Date: 2025-10-30 11:48:55.261631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from src.models.site_config_model import SiteConfig


# revision identifiers, used by Alembic.
revision: str = '1090551e7519'
down_revision: Union[str, Sequence[str], None] = '546f9fbd9cb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    SiteConfig.__table__.create(op.get_bind(), checkfirst=True)

    pass


def downgrade() -> None:
    """Downgrade schema."""

    SiteConfig.__table__.drop(op.get_bind(), checkfirst=True)

    pass
