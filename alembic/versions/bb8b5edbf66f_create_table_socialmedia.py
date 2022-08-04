"""create table socialmedia

Revision ID: bb8b5edbf66f
Revises: 
Create Date: 2022-08-03 14:03:05.197982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb8b5edbf66f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:   #to make changes in the table
    op.create_table("social media", sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                     sa.Column('title', sa.String(), nullable=False))
    


def downgrade() -> None: # to rollback changes.
    op.drop_table("social media")
