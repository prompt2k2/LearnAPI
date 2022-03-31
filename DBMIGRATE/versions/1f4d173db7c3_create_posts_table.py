"""create posts table

Revision ID: 1f4d173db7c3
Revises: 
Create Date: 2022-03-31 11:53:37.753698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f4d173db7c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
        sa.Column('title', sa.String(), nullable=False), 
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('published', sa.Boolean(), nullable=False),)
    pass


def downgrade():
    op.drop_table('posts')
    pass
