"""create posts table

Revision ID: 529c2344218a
Revises: 
Create Date: 2023-03-21 18:06:28.508874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '529c2344218a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
