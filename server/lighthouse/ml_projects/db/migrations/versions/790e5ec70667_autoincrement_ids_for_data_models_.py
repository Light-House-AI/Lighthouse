"""autoincrement ids for data, models & deployments

Revision ID: 790e5ec70667
Revises: 9ca536a0a427
Create Date: 2022-05-19 23:25:03.657132

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import Sequence, CreateSequence, DropSequence

# revision identifiers, used by Alembic.
revision = '790e5ec70667'
down_revision = '9ca536a0a427'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(CreateSequence(Sequence('data_version_seq')))

    op.alter_column('data',
                    'version',
                    server_default=sa.text('nextval(\'data_version_seq\')'))

    op.execute(CreateSequence(Sequence('model_version_seq')))
    op.alter_column('model',
                    'version',
                    server_default=sa.text('nextval(\'model_version_seq\')'))

    op.execute(CreateSequence(Sequence('deployment_id_seq')))
    op.alter_column('deployment',
                    'id',
                    server_default=sa.text('nextval(\'deployment_id_seq\')'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('deployment', 'id', server_default=None)
    op.alter_column('model', 'version', server_default=None)
    op.alter_column('data', 'version', server_default=None)

    op.execute("drop sequence deployment_id_seq")
    op.execute("drop sequence model_version_seq")
    op.execute("drop sequence data_version_seq")
    # ### end Alembic commands ###
