"""auto-vote

Revision ID: a13fc1e37c8d
Revises: 1eaff34a94dd
Create Date: 2023-03-22 13:53:25.663436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a13fc1e37c8d'
down_revision = '1eaff34a94dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    #Sugenerravo pagal models.py, paleidus komanda: alembic revision --autogenerate -m "auto-vote"
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###