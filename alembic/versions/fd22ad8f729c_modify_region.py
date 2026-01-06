"""modify region

Revision ID: fd22ad8f729c
Revises: 6e2f3a5dcd0f
Create Date: 2026-01-05 19:04:45.026987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd22ad8f729c'
down_revision: Union[str, Sequence[str], None] = '6e2f3a5dcd0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("players", sa.Column("platform", sa.String(length=15), nullable=True))

    # backfill: tutti i player EU → EUROPE
    op.execute("UPDATE players SET platform = 'EUW1' WHERE platform IS NULL")

    op.alter_column("players", "platform", nullable=False)



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('players', 'platform')
