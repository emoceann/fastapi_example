"""init

Revision ID: 9866573f035d
Revises: 
Create Date: 2023-08-20 07:37:17.461210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9866573f035d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=1024), nullable=True),
    sa.Column('password', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###