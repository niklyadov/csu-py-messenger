"""Поменяли password на hashed_password

Revision ID: 8cc07bbfb7e7
Revises: b49cfbd7a2f7
Create Date: 2022-05-18 17:36:25.498747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cc07bbfb7e7'
down_revision = 'b49cfbd7a2f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('hashed_password', sa.String(120), nullable=True))
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.VARCHAR(120), autoincrement=False, nullable=True))
    op.drop_column('users', 'hashed_password')
    # ### end Alembic commands ###
