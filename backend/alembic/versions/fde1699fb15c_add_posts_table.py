"""add posts table

Revision ID: fde1699fb15c
Revises: a085dc354b40
Create Date: 2026-09-17 16:22:12.951501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fde1699fb15c'
down_revision: Union[str, Sequence[str], None] = 'a085dc354b40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('movie_id', sa.Integer(), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('watch_if_you_enjoyed', sa.Text(), nullable=True),
        sa.Column('favourite_character', sa.Text(), nullable=True),
        sa.Column('favourite_part', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_posts_user_id'), 'posts', ['user_id'], unique=False)
    op.create_index(op.f('ix_posts_movie_id'), 'posts', ['movie_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_posts_movie_id'), table_name='posts')
    op.drop_index(op.f('ix_posts_user_id'), table_name='posts')
    op.drop_table('posts')