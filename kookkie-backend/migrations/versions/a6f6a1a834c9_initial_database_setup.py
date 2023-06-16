"""Initial database setup

Revision ID: a6f6a1a834c9
Revises: 
Create Date: 2023-06-10 17:58:42.657803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6f6a1a834c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kook',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=140), nullable=True),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('hashed_password', sa.String(length=140), nullable=True),
    sa.Column('password_reset_token', sa.String(length=140), nullable=True),
    sa.Column('password_reset_token_created_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('kook', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_kook_email'), ['email'], unique=False)
        batch_op.create_index(batch_op.f('ix_kook_password_reset_token'), ['password_reset_token'], unique=False)

    op.create_table('kookkie_session',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('date', sa.String(length=140), nullable=True),
    sa.Column('kook_id', sa.String(length=140), nullable=True),
    sa.Column('kook_name', sa.String(length=140), nullable=True),
    sa.Column('open', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('kookkie_session', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_kookkie_session_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_kookkie_session_kook_id'), ['kook_id'], unique=False)

    op.create_table('kookkie_participant',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('joining_id', sa.String(length=40), nullable=True),
    sa.Column('kookkie_session_id', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=True),
    sa.ForeignKeyConstraint(['kookkie_session_id'], ['kookkie_session.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('kookkie_participant')
    with op.batch_alter_table('kookkie_session', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_kookkie_session_kook_id'))
        batch_op.drop_index(batch_op.f('ix_kookkie_session_created_at'))

    op.drop_table('kookkie_session')
    with op.batch_alter_table('kook', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_kook_password_reset_token'))
        batch_op.drop_index(batch_op.f('ix_kook_email'))

    op.drop_table('kook')
    # ### end Alembic commands ###
