# this file will instruct alembic how to generate new migration scripts

"""Create Profiles table
Revision ID: 54384922668d
Revises: 51e10b2d01ef
Create Date: 2021-10-04 17:04:21.070969
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '54384922668d'
down_revision = '51e10b2d01ef'
branch_labels = None
depends_on = None
def upgrade() -> None:
    pass
def downgrade() -> None:
    pass
