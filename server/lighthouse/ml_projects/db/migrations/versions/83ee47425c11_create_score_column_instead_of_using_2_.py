"""create score column instead of using 2 columns

Revision ID: 83ee47425c11
Revises: 94deb3e05eb3
Create Date: 2022-06-20 21:35:45.783951

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '83ee47425c11'
down_revision = '94deb3e05eb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('model', sa.Column('score', sa.Float(), nullable=True))
    op.drop_column('model', 'accuracy_score')
    op.drop_column('model', 'mean_squared_log_error')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('model', sa.Column('mean_squared_log_error', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('model', sa.Column('accuracy_score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('model', 'score')
    # ### end Alembic commands ###
