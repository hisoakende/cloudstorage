"""add the unique constraints to file model and size field

Revision ID: 479e292c3a49
Revises: ce640faf35d3
Create Date: 2023-04-20 12:21:36.979227

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = '479e292c3a49'
down_revision = 'ce640faf35d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('size', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'file', ['location'])
    # ### end Alembic commands ###
    op.execute('ALTER TABLE file ADD CONSTRAINT file_name_directory_id '
               'UNIQUE NULLS NOT DISTINCT ("name", "directory_id")')


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('file', 'size')
    op.drop_constraint('file_location_key', 'file', type_='unique')
    # ### end Alembic commands ###
    op.execute('ALTER TABLE file DROP CONSTRAINT file_name_directory_id')