"""create table email sms temp rest payment rating

Revision ID: 22fed7299a91
Revises: ecffeccb65ea
Create Date: 2025-11-06 16:24:33.619873

"""
from src.models.template_model import EmailTemplateModel, SMSTemplateModel
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22fed7299a91'
down_revision: Union[str, Sequence[str], None] = 'ecffeccb65ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    bind = op.get_bind()
    EmailTemplateModel.__table__.create(bind, checkfirst=True)
    SMSTemplateModel.__table__.create(bind, checkfirst=True)

    pass


def downgrade() -> None:
    """Downgrade schema."""

    bind = op.get_bind()
    EmailTemplateModel.__table__.drop(bind, checkfirst=True)
    SMSTemplateModel.__table__.drop(bind, checkfirst=True)

    pass
