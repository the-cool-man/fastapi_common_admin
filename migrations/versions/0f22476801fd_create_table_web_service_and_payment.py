"""create table web_service payment

Revision ID: 0f22476801fd
Revises: 22fed7299a91
Create Date: 2025-11-06 17:02:28.406232

"""
from src.models.web_payment_model import WebServiceModel, UserPaymentModel
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f22476801fd'
down_revision: Union[str, Sequence[str], None] = '22fed7299a91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    WebServiceModel.__table__.create(bind, checkfirst=True)
    UserPaymentModel.__table__.create(bind, checkfirst=True)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    
    bind = op.get_bind()

    WebServiceModel.__table__.drop(bind, checkfirst=True)
    UserPaymentModel.__table__.drop(bind, checkfirst=True)
    pass
