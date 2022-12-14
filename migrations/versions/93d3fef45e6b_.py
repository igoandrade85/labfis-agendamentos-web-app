"""empty message

Revision ID: 93d3fef45e6b
Revises: f93346d3ff2f
Create Date: 2022-08-22 12:33:39.651809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93d3fef45e6b'
down_revision = 'f93346d3ff2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agendamentos', sa.Column('descricao_atividades', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('agendamentos', 'descricao_atividades')
    # ### end Alembic commands ###
