"""create tables

Revision ID: c84ccda7c459
Revises: 3ced1dabd6dc
Create Date: 2022-08-17 23:09:34.896311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c84ccda7c459'
down_revision = '3ced1dabd6dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=120), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('rating', sa.Numeric(precision=1, scale=2), nullable=True),
    sa.Column('no_of_ratings', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_product_name'), 'product', ['product_name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_product_product_name'), table_name='product')
    op.drop_table('product')
    # ### end Alembic commands ###
