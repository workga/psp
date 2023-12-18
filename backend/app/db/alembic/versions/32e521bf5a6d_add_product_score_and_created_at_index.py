"""add_product_score_and_created_at_index

Revision ID: 32e521bf5a6d
Revises: 9c0b0cfe13fb
Create Date: 2023-12-18 20:32:25.850638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32e521bf5a6d'
down_revision: Union[str, None] = '9c0b0cfe13fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('score', sa.Integer(), server_default=sa.text('0'), nullable=False))
    op.create_index(op.f('ix_product_price'), 'product', ['price'], unique=False)
    op.create_index(op.f('ix_product_score'), 'product', ['score'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_product_score'), table_name='product')
    op.drop_index(op.f('ix_product_price'), table_name='product')
    op.drop_column('product', 'score')
    # ### end Alembic commands ###
