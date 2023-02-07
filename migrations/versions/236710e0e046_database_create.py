"""database create

Revision ID: 236710e0e046
Revises: 
Create Date: 2023-02-07 00:14:39.568782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '236710e0e046'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('created', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=128), nullable=True),
    sa.Column('last_name', sa.String(length=128), nullable=True),
    sa.Column('photo', sa.LargeBinary(), nullable=True),
    sa.Column('photo_50', sa.LargeBinary(), nullable=True),
    sa.Column('photo_100', sa.LargeBinary(), nullable=True),
    sa.Column('photo_400', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profile')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
