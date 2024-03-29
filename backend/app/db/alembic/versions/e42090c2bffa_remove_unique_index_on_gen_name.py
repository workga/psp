"""remove_unique_index_on_gen_name

Revision ID: e42090c2bffa
Revises: 50b0aa9b2c66
Create Date: 2023-11-01 03:06:41.498435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e42090c2bffa'
down_revision: Union[str, None] = '50b0aa9b2c66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_car_gen_gen_name', table_name='car_gen')
    op.create_index(op.f('ix_car_gen_gen_name'), 'car_gen', ['gen_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_car_gen_gen_name'), table_name='car_gen')
    op.create_index('ix_car_gen_gen_name', 'car_gen', ['gen_name'], unique=False)
    # ### end Alembic commands ###
