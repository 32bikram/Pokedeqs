"""pgtrgm for neo_db

Revision ID: 05f80dec4c0e
Revises: 
Create Date: 2026-08-09 18:16:29.311149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05f80dec4c0e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    pass


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS pg_trgm;")
    pass
