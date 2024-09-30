"""empty message

Revision ID: 9a784511696c
Revises: c8827d1f8799
Create Date: 2024-09-30 15:42:35.245025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a784511696c'
down_revision = 'c8827d1f8799'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.drop_column('rotation_period')
        batch_op.drop_column('population')
        batch_op.drop_column('orbital_period')
        batch_op.drop_column('gravity')
        batch_op.drop_column('surface_water')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('surface_water', sa.VARCHAR(length=10), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('gravity', sa.VARCHAR(length=10), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('orbital_period', sa.VARCHAR(length=10), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('population', sa.VARCHAR(length=10), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('rotation_period', sa.VARCHAR(length=10), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
