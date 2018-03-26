"""empty message

Revision ID: bf8c7575e3d1
Revises: 2ff7e9085a54
Create Date: 2018-03-25 19:18:33.382945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf8c7575e3d1'
down_revision = '2ff7e9085a54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('due_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'due_date')
    # ### end Alembic commands ###
