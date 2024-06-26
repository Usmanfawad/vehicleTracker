"""Add last_bus_stop to bus

Revision ID: 8f48148be609
Revises: 3f2a86923ebc
Create Date: 2024-05-08 14:41:38.558710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f48148be609'
down_revision: Union[str, None] = '3f2a86923ebc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bus', sa.Column('last_stop_index', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bus', 'last_stop_index')
    # ### end Alembic commands ###
