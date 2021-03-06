"""empty message

Revision ID: 27a7f777c09c
Revises: 80df60e6945d
Create Date: 2018-11-13 19:17:17.293110

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '27a7f777c09c'
down_revision = '80df60e6945d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'user_type',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
    op.alter_column('users', 'username',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('users', 'user_type',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
    # ### end Alembic commands ###
