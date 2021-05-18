"""empty message

Revision ID: c1197755e22a
Revises: 06114281aae8
Create Date: 2021-03-31 20:04:00.362858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c1197755e22a"
down_revision = "06114281aae8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("genome", sa.Column("reverse_complement", sa.String(), nullable=True))
    op.add_column("genome", sa.Column("rna_transcription", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("genome", "rna_transcription")
    op.drop_column("genome", "reverse_complement")
    # ### end Alembic commands ###