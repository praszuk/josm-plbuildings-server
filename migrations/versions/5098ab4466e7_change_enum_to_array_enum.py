"""Change Enum to Array Enum

Revision ID: 5098ab4466e7
Revises: cef6f13620e6
Create Date: 2022-11-01 17:58:32.637690

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5098ab4466e7'
down_revision = 'cef6f13620e6'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'buildings_logs',
        'data_source',
        new_column_name='data_sources',
        type_=sa.ARRAY(sa.Enum('BDOT', 'EGIB', name='buildingsdatasource')),
        postgresql_using='ARRAY[data_source]'
    )


def downgrade():
    op.alter_column(
        'buildings_logs',
        'data_sources',
        new_column_name='data_source',
        type_=sa.Enum('BDOT', 'EGIB', name='buildingsdatasource'),
        postgresql_using='data_sources[1]'
    )
