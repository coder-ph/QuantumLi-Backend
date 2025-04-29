"""Merge multiple heads

Revision ID: d94f2e67f607
Revises: 3bc5de381af7, ea20465d82ef
Create Date: 2025-04-29 18:12:25.183000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd94f2e67f607'
down_revision = ('3bc5de381af7', 'ea20465d82ef')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
