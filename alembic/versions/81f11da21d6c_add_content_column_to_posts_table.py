"""add content column to posts table

Revision ID: 81f11da21d6c
Revises: 529c2344218a
Create Date: 2023-03-22 12:35:49.315285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81f11da21d6c'
down_revision = '529c2344218a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
