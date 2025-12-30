"""add jwt refresh tokens and link sessions

Revision ID: 2f9f18a4e2d1
Revises: 9cdb66a84d52
Create Date: 2025-12-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2f9f18a4e2d1"
down_revision: Union[str, None] = "9cdb66a84d52"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "jwt",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("token", sa.String(length=1024), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "tg_bot_auth",
        sa.Column("jwt_token_id", sa.Uuid(), nullable=True),
    )
    op.create_foreign_key(
        "tg_bot_auth_jwt_token_id_fkey",
        "tg_bot_auth",
        "jwt",
        ["jwt_token_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "tg_bot_auth_jwt_token_id_fkey",
        "tg_bot_auth",
        type_="foreignkey",
    )
    op.drop_column("tg_bot_auth", "jwt_token_id")
    op.drop_table("jwt")
