"""add_content_to_posts

Revision ID: 3ce5edbf6fb2
Revises: d1922982a9a2
Create Date: 2023-11-08 07:00:32.159463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ce5edbf6fb2'
down_revision: Union[str, None] = 'd1922982a9a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts' ,sa.Column('content' ,sa.String() ,nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts' ,'content')
    pass
