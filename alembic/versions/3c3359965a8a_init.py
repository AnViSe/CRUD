"""Init

Revision ID: 3c3359965a8a
Revises: 
Create Date: 2021-12-17 11:07:45.793923+03:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c3359965a8a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currencies',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('code', sa.String(length=3), nullable=False),
    sa.Column('scale', sa.Integer(), server_default='1', nullable=False),
    sa.Column('rate', sa.Numeric(precision=10, scale=5), nullable=False),
    sa.Column('date_start', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('currency_uq01', 'currencies', ['code', 'date_start'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('username', sa.String(length=70), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=70), nullable=True),
    sa.Column('balance', sa.Numeric(precision=10, scale=2), server_default='0', nullable=False),
    sa.Column('banker', sa.Boolean(), server_default='False', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('invoices',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), nullable=False),
    sa.Column('inv_date', sa.Date(), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.Column('curr_count', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('status', sa.Enum('progress', 'accept', 'reject', name='statuses'), nullable=False),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invoices')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    op.drop_index('currency_uq01', table_name='currencies')
    op.drop_table('currencies')
    op.get_bind().execute('DROP TYPE statuses')
    # ### end Alembic commands ###
