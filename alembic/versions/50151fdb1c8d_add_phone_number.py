"""add_phone_number

Revision ID: 50151fdb1c8d
Revises: 4ff2fea42fd3
Create Date: 2023-11-08 07:12:03.281235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50151fdb1c8d'
down_revision: Union[str, None] = '4ff2fea42fd3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users' ,sa.Column('phone_number' ,sa.String() ,nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('users' ,'phone_number')
    pass
