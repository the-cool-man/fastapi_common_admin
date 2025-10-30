"""create social_media_link and public_page_seo

Revision ID: 1b317cd22a75
Revises: 1090551e7519
Create Date: 2025-10-30 12:03:39.226140

"""
from src.models.site_config_model import SocialMedia, PublicPageSEO
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b317cd22a75'
down_revision: Union[str, Sequence[str], None] = '1090551e7519'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    SocialMedia.__table__.create(bind, checkfirst=True)
    PublicPageSEO.__table__.create(bind, checkfirst=True)

    pass


def downgrade() -> None:
    """Downgrade schema."""

    bind = op.get_bind()
    SocialMedia.__table__.drop(bind, checkfirst=True)
    PublicPageSEO.__table__.drop(bind, checkfirst=True)

    pass
