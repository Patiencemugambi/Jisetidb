"""initial migration

Revision ID: 3edeba1064a9
Revises: 
Create Date: 2023-11-06 11:00:21.884859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3edeba1064a9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('record_type', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('admin_actions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('record_id', sa.Integer(), nullable=True),
    sa.Column('action', sa.String(), nullable=True),
    sa.Column('timestamp', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('interventions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('attachments', sa.String(), nullable=True),
    sa.Column('additional_details', sa.Text(), nullable=True),
    sa.Column('county', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['status_id'], ['statuses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('logins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_logins_email'), 'logins', ['email'], unique=True)
    op.create_index(op.f('ix_logins_id'), 'logins', ['id'], unique=False)
    op.create_index(op.f('ix_logins_username'), 'logins', ['username'], unique=True)
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('is_email', sa.Boolean(), nullable=True),
    sa.Column('is_sms', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('red_flags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('incident_type', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('attachments', sa.String(), nullable=True),
    sa.Column('additional_details', sa.Text(), nullable=True),
    sa.Column('county', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['status_id'], ['statuses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_red_flags_id'), 'red_flags', ['id'], unique=False)
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('red_flag_id', sa.Integer(), nullable=True),
    sa.Column('intervention_id', sa.Integer(), nullable=True),
    sa.Column('file_path', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['intervention_id'], ['interventions.id'], ),
    sa.ForeignKeyConstraint(['red_flag_id'], ['red_flags.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('red_flag_id', sa.Integer(), nullable=True),
    sa.Column('intervention_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['intervention_id'], ['interventions.id'], ),
    sa.ForeignKeyConstraint(['red_flag_id'], ['red_flags.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('red_flag_id', sa.Integer(), nullable=True),
    sa.Column('intervention_id', sa.Integer(), nullable=True),
    sa.Column('file_path', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['intervention_id'], ['interventions.id'], ),
    sa.ForeignKeyConstraint(['red_flag_id'], ['red_flags.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('videos')
    op.drop_table('tags')
    op.drop_table('images')
    op.drop_index(op.f('ix_red_flags_id'), table_name='red_flags')
    op.drop_table('red_flags')
    op.drop_table('notifications')
    op.drop_index(op.f('ix_logins_username'), table_name='logins')
    op.drop_index(op.f('ix_logins_id'), table_name='logins')
    op.drop_index(op.f('ix_logins_email'), table_name='logins')
    op.drop_table('logins')
    op.drop_table('interventions')
    op.drop_table('admin_actions')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('statuses')
    # ### end Alembic commands ###