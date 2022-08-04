"""add column to social media

Revision ID: be4e6dc7b0e1
Revises: bb8b5edbf66f
Create Date: 2022-08-03 14:20:42.994420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be4e6dc7b0e1'
down_revision = 'bb8b5edbf66f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("social media", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("social media", "content")
    pass
