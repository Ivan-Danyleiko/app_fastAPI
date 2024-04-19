"""Init

Revision ID: 7713b3b23af5
Revises: 
Create Date: 2024-04-19 09:20:55.701889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7713b3b23af5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.Column('lastname', sa.String(length=25), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=False),
    sa.Column('done', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('contact_note_association',
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.Column('note_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['note_id'], ['notes.id'], ondelete='CASCADE')
    )
    op.create_table('note_tag_association',
    sa.Column('note_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['note_id'], ['notes.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('note_tag_association')
    op.drop_table('contact_note_association')
    op.drop_table('tags')
    op.drop_table('notes')
    op.drop_table('contacts')
    # ### end Alembic commands ###
