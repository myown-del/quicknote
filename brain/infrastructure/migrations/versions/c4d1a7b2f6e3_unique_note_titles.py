"""make note titles unique and non-null

Revision ID: c4d1a7b2f6e3
Revises: b9a62f1c9b12
Create Date: 2026-01-01 00:00:00.000000

"""
from typing import Sequence, Union
from uuid import UUID, uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c4d1a7b2f6e3"
down_revision: Union[str, None] = "b9a62f1c9b12"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _next_untitled(used_titles: set[str]) -> str:
    index = 1
    while True:
        candidate = f"Untitled {index}"
        if candidate not in used_titles:
            return candidate
        index += 1


def _next_duplicate_title(used_titles: set[str], base: str) -> str:
    index = 2
    while True:
        candidate = f"{base} ({index})"
        if candidate not in used_titles:
            return candidate
        index += 1


def upgrade() -> None:
    bind = op.get_bind()
    notes = sa.table(
        "notes",
        sa.column("id", sa.Uuid()),
        sa.column("user_id", sa.Uuid()),
        sa.column("title", sa.String()),
        sa.column("represents_keyword_id", sa.Uuid()),
    )
    keywords = sa.table(
        "keywords",
        sa.column("id", sa.Uuid()),
        sa.column("user_id", sa.Uuid()),
        sa.column("name", sa.String()),
    )

    keyword_rows = bind.execute(
        sa.select(keywords.c.id, keywords.c.user_id, keywords.c.name)
    ).fetchall()
    keyword_map = {(row[1], row[2]): row[0] for row in keyword_rows}

    note_rows = bind.execute(
        sa.select(notes.c.id, notes.c.user_id, notes.c.title)
        .order_by(notes.c.user_id, notes.c.id)
    ).fetchall()

    used_titles_by_user: dict[UUID, set[str]] = {}
    new_keywords: list[dict[str, object]] = []
    updates: list[dict[str, object]] = []

    for note_id, user_id, title in note_rows:
        used_titles = used_titles_by_user.setdefault(user_id, set())
        if title is None:
            title = _next_untitled(used_titles)
        elif title in used_titles:
            title = _next_duplicate_title(used_titles, title)
        used_titles.add(title)

        keyword_key = (user_id, title)
        if keyword_key not in keyword_map:
            keyword_id = uuid4()
            keyword_map[keyword_key] = keyword_id
            new_keywords.append(
                {"id": keyword_id, "user_id": user_id, "name": title}
            )

        updates.append(
            {
                "note_id": note_id,
                "title": title,
                "keyword_id": keyword_map[keyword_key],
            }
        )

    if new_keywords:
        bind.execute(keywords.insert(), new_keywords)

    if updates:
        bind.execute(
            notes.update()
            .where(notes.c.id == sa.bindparam("note_id"))
            .values(
                title=sa.bindparam("title"),
                represents_keyword_id=sa.bindparam("keyword_id"),
            ),
            updates,
        )

    op.alter_column("notes", "title", existing_type=sa.String(length=255), nullable=False)
    op.create_unique_constraint(
        "uq_notes_user_id_title",
        "notes",
        ["user_id", "title"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_notes_user_id_title", "notes", type_="unique")
    op.alter_column("notes", "title", existing_type=sa.String(length=255), nullable=True)
