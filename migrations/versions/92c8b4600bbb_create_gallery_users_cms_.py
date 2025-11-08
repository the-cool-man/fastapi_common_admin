"""photo_gallery, users, users_details, cms_pages

Revision ID: 92c8b4600bbb
Revises: 3cdcdb6638a4
Create Date: 2025-11-03 12:13:17.875588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from src.models.users_content_model import OrdinaryUserModel, OrdinaryUserDetailModel, MediaGalleryModel, CmsPageModel, OrdinaryUserRatingModel


# revision identifiers, used by Alembic.
revision: str = '92c8b4600bbb'
down_revision: Union[str, Sequence[str], None] = '3cdcdb6638a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    OrdinaryUserModel.__table__.create(bind, checkfirst=True)
    OrdinaryUserDetailModel.__table__.create(bind, checkfirst=True)
    MediaGalleryModel.__table__.create(bind, checkfirst=True)
    CmsPageModel.__table__.create(bind, checkfirst=True)
    OrdinaryUserRatingModel.__table__.create(bind, checkfirst=True)

    pass


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    OrdinaryUserModel.__table__.drop(bind, checkfirst=True)
    OrdinaryUserDetailModel.__table__.drop(bind, checkfirst=True)
    MediaGalleryModel.__table__.drop(bind, checkfirst=True)
    CmsPageModel.__table__.drop(bind, checkfirst=True)
    OrdinaryUserRatingModel.__table__.drop(bind, checkfirst=True)
    pass
