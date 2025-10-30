"""create master_section

Revision ID: 1599e5e32aea
Revises: 1b317cd22a75
Create Date: 2025-10-30 12:36:31.540849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from src.models.master_model import BannerModel, CategoryModel, CurrencyModel, GstPercentageModel


# revision identifiers, used by Alembic.
revision: str = '1599e5e32aea'
down_revision: Union[str, Sequence[str], None] = '1b317cd22a75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    BannerModel.__table__.create(bind, checkfirst=True)
    CategoryModel.__table__.create(bind, checkfirst=True)
    CurrencyModel.__table__.create(bind, checkfirst=True)
    GstPercentageModel.__table__.create(bind, checkfirst=True)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()

    BannerModel.__table__.drop(bind, checkfirst=True)
    CategoryModel.__table__.drop(bind, checkfirst=True)
    CurrencyModel.__table__.drop(bind, checkfirst=True)
    GstPercentageModel.__table__.drop(bind, checkfirst=True)
    pass
