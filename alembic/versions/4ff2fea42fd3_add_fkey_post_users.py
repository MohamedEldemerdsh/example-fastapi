"""add_fkey_post_users

Revision ID: 4ff2fea42fd3
Revises: 30f64d3d66d0
Create Date: 2023-11-08 07:07:44.229345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ff2fea42fd3'
down_revision: Union[str, None] = '30f64d3d66d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts' ,sa.Column('owner_id' ,sa.Integer() ,nullable=False))
    op.create_foreign_key('post_users_fkey' ,source_table="posts" ,referent_table="users" ,
                          local_cols=['owner_id'] ,remote_cols=['id'] ,ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fkey' ,table_name="posts")
    op.drop_column('posts' ,'owner_id')
    pass
