"""seed admin_role data

Revision ID: 79bc78a31b85
Revises: 379fd34a16b6
Create Date: 2025-10-05 17:02:00.926108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79bc78a31b85'
down_revision: Union[str, Sequence[str], None] = '379fd34a16b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text("""
        INSERT INTO admin_role 
        (id, status, role_name, site_setting, banner, category, currency, tax_data, country, state, city,
         media_gallery, all_user, chat, rating, site_content, email_template, sms_template, rest_api,
         payment_plan, created_at, updated_at, deleted_at)
        VALUES
        (1, 'A', 'Super Admin', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', '2023-10-16 05:52:38', NULL, NULL),
        (2, 'A', 'Staff Role', 'Y', 'Y', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', '2023-10-16 23:06:07', '2023-10-27 14:21:06', NULL),
        (3, 'A', 'Test Staff Role', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', '2023-10-17 15:46:47', '2023-10-26 11:26:23', NULL),
        (14, 'A', 'new Test Staff Role', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', '2023-10-17 15:46:47', '2023-10-26 11:26:23', NULL),
        (15, 'I', 'test', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', '2025-02-24 17:02:46', NULL, '2025-02-24 17:03:13'),
        (16, 'A', 'new test', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', '2025-02-24 17:03:46', '2025-02-24 17:07:57', '2025-02-24 17:08:29'),
        (17, 'A', 'new test role', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', '2025-02-24 17:45:54', '2025-02-24 17:50:14', NULL),
        (18, 'A', 'User 1', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', '2025-03-04 10:05:29', NULL, NULL)
        """)
    )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(sa.text("DELETE FROM admin_role"))
