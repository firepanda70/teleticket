"""base

Revision ID: 8fce3f84fcab
Revises: 
Create Date: 2023-12-28 07:03:10.962100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fce3f84fcab'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('user_pkey'))
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('user_email_idx'), ['email'], unique=True)

    op.create_table('ticket',
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('tg_user_id', sa.Integer(), nullable=False),
    sa.Column('support_user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['support_user_id'], ['user.id'], name=op.f('ticket_support_user_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('ticket_pkey'))
    )
    op.create_table('message',
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('from_client', sa.Boolean(), nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=False),
    sa.Column('support_user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['support_user_id'], ['user.id'], name=op.f('message_support_user_id_fkey')),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.id'], name=op.f('message_ticket_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('message_pkey'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    op.drop_table('ticket')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('user_email_idx'))

    op.drop_table('user')
    # ### end Alembic commands ###
