"""create country, state, and city

Revision ID: 3cdcdb6638a4
Revises: 1599e5e32aea
Create Date: 2025-10-31 11:19:43.926159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from src.models.master_model import CountryModel, StateModel, CityModel


# revision identifiers, used by Alembic.
revision: str = '3cdcdb6638a4'
down_revision: Union[str, Sequence[str], None] = '1599e5e32aea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    CountryModel.__table__.create(op.get_bind(), checkfirst=True)
    StateModel.__table__.create(op.get_bind(), checkfirst=True)
    CityModel.__table__.create(op.get_bind(), checkfirst=True)

    pass


def downgrade() -> None:
    """Downgrade schema."""
    CountryModel.__table__.drop(op.get_bind(), checkfirst=True)
    StateModel.__table__.drop(op.get_bind(), checkfirst=True)
    CityModel.__table__.drop(op.get_bind(), checkfirst=True)

    pass
