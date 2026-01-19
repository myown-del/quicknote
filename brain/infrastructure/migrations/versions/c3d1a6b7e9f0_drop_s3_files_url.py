"""Drop persisted S3 file url

Revision ID: c3d1a6b7e9f0
Revises: f9b5664042eb
Create Date: 2026-01-20 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c3d1a6b7e9f0"
down_revision: Union[str, None] = "f9b5664042eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("s3_files", "url")


def downgrade() -> None:
    op.add_column(
        "s3_files",
        sa.Column("url", sa.String(length=2048), nullable=False),
    )
