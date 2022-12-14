"""empty message

Revision ID: 529098aec069
Revises: 
Create Date: 2022-07-29 08:25:15.212029

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '529098aec069'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userDB',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('gender', sa.Enum('Pria', 'Perempuan', name='gender'), nullable=True),
    sa.Column('birthdate', sa.Date(), nullable=False),
    sa.Column('created_datetime', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_datetime', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('activityDB',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('check_in', sa.Time(), nullable=True),
    sa.Column('activity', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('IN_QUEUE', 'DONE', 'CANCELLED', name='status'), nullable=True),
    sa.Column('check_out', sa.Time(), nullable=True),
    sa.Column('created_datetime', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_datetime', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['userDB.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('activityDB')
    op.drop_table('userDB')
    # ### end Alembic commands ###
