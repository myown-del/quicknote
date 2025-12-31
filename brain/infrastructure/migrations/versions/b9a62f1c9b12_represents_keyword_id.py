"""add represents_keyword_id to notes

Revision ID: b9a62f1c9b12
Revises: a636247b1e01
Create Date: 2025-12-31 18:40:00.000000

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b9a62f1c9b12"
down_revision: Union[str, None] = "a636247b1e01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "notes",
        sa.Column("represents_keyword_id", sa.Uuid(), nullable=True),
    )
    op.create_foreign_key(
        "fk_notes_represents_keyword_id",
        "notes",
        "keywords",
        ["represents_keyword_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="SET NULL",
    )
    op.create_unique_constraint(
        "uq_notes_represents_keyword_id",
        "notes",
        ["represents_keyword_id"],
    )

    bind = op.get_bind()
    notes = sa.table(
        "notes",
        sa.column("user_id", sa.Uuid()),
        sa.column("title", sa.String()),
        sa.column("represents_keyword", sa.Boolean()),
    )
    keywords = sa.table(
        "keywords",
        sa.column("id", sa.Uuid()),
        sa.column("user_id", sa.Uuid()),
        sa.column("name", sa.String()),
    )

    result = bind.execute(
        sa.select(notes.c.user_id, notes.c.title)
        .where(notes.c.represents_keyword.is_(True))
        .where(notes.c.title.isnot(None))
        .where(sa.func.length(sa.func.trim(notes.c.title)) > 0)
    )
    pairs = {(row[0], row[1]) for row in result.fetchall()}
    if pairs:
        existing = bind.execute(
            sa.select(keywords.c.user_id, keywords.c.name)
            .where(sa.tuple_(keywords.c.user_id, keywords.c.name).in_(pairs))
        )
        existing_pairs = {(row[0], row[1]) for row in existing.fetchall()}
        missing = pairs - existing_pairs
        if missing:
            bind.execute(
                keywords.insert(),
                [{"id": uuid4(), "user_id": user_id, "name": name} for user_id, name in missing],
            )

        bind.execute(
            sa.text(
                "UPDATE notes "
                "SET represents_keyword_id = keywords.id "
                "FROM keywords "
                "WHERE notes.user_id = keywords.user_id "
                "AND notes.title = keywords.name "
                "AND notes.represents_keyword = true"
            )
        )

    op.drop_column("notes", "represents_keyword")


def downgrade() -> None:
    op.add_column(
        "notes",
        sa.Column(
            "represents_keyword",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )
    op.execute(
        sa.text(
            "UPDATE notes SET represents_keyword = true "
            "WHERE represents_keyword_id IS NOT NULL"
        )
    )
    op.drop_constraint(
        "fk_notes_represents_keyword_id",
        "notes",
        type_="foreignkey",
    )
    op.drop_constraint(
        "uq_notes_represents_keyword_id",
        "notes",
        type_="unique",
    )
    op.drop_column("notes", "represents_keyword_id")
