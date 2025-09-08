"""add image_url to transactions

Revision ID: 1234567890ab
Revises: 
Create Date: 2025-08-22 10:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1234567890ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add image_url column to transactions table
    op.add_column('transactions', sa.Column('image_url', sa.String(), nullable=True))


def downgrade():
    # Remove image_url column from transactions table
    op.drop_column('transactions', 'image_url')
