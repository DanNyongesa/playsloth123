"""empty message

Revision ID: 14d76a10995c
Revises: 
Create Date: 2017-03-02 11:39:50.449000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14d76a10995c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('albums',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist', sa.String(length=250), nullable=True),
    sa.Column('album_title', sa.String(length=250), nullable=True),
    sa.Column('genre', sa.String(length=100), nullable=True),
    sa.Column('album_logo', sa.String(length=250), nullable=True),
    sa.Column('logo_url', sa.String(), nullable=True),
    sa.Column('is_favorite', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=20), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('songs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('song_title', sa.String(), nullable=True),
    sa.Column('audio_file', sa.String(), nullable=True),
    sa.Column('audio_url', sa.String(), nullable=True),
    sa.Column('is_favorite', sa.Boolean(), nullable=True),
    sa.Column('album_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['albums.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('songs')
    op.drop_table('users')
    op.drop_table('albums')
    # ### end Alembic commands ###
