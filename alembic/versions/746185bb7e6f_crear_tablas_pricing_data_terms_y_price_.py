"""Crear tablas pricing_data, terms, y price_dimensions

Revision ID: 746185bb7e6f
Revises: 
Create Date: 2025-03-31 20:20:25.287789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '746185bb7e6f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pricing_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sku', sa.String(), nullable=False),
    sa.Column('product_family', sa.String(), nullable=True),
    sa.Column('database_engine', sa.String(), nullable=True),
    sa.Column('instance_type', sa.String(), nullable=True),
    sa.Column('memory', sa.String(), nullable=True),
    sa.Column('vcpu', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sku')
    )
    op.create_index(op.f('ix_pricing_data_id'), 'pricing_data', ['id'], unique=False)
    op.create_table('terms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sku', sa.String(), nullable=True),
    sa.Column('offerTermCode', sa.String(), nullable=True),
    sa.Column('effectiveDate', sa.TIMESTAMP(), nullable=True),
    sa.Column('termType', sa.String(), nullable=True),
    sa.Column('leaseContractLength', sa.String(), nullable=True),
    sa.Column('purchaseOption', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['sku'], ['pricing_data.sku'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_terms_id'), 'terms', ['id'], unique=False)
    op.create_table('price_dimensions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('term_id', sa.Integer(), nullable=True),
    sa.Column('rateCode', sa.String(), nullable=True),
    sa.Column('unit', sa.String(), nullable=True),
    sa.Column('beginRange', sa.Numeric(), nullable=True),
    sa.Column('endRange', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('priceUSD', sa.Numeric(), nullable=True),
    sa.ForeignKeyConstraint(['term_id'], ['terms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_price_dimensions_id'), 'price_dimensions', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_price_dimensions_id'), table_name='price_dimensions')
    op.drop_table('price_dimensions')
    op.drop_index(op.f('ix_terms_id'), table_name='terms')
    op.drop_table('terms')
    op.drop_index(op.f('ix_pricing_data_id'), table_name='pricing_data')
    op.drop_table('pricing_data')
    # ### end Alembic commands ###
