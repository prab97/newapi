"""add phone

Revision ID: b2b6a863017f
Revises: c8ea2a0acabd
Create Date: 2022-08-03 17:48:25.815080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2b6a863017f'
down_revision = 'c8ea2a0acabd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_no', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_no')
    # ### end Alembic commands ###
