"""add content column to post table

Revision ID: 80a59708396b
Revises: 452341cc27ec
Create Date: 2026-04-02 19:01:51.695012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80a59708396b'
down_revision: Union[str, Sequence[str], None] = '452341cc27ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
