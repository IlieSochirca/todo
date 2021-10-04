# this file will instruct alembic how to generate new migration scripts

"""Create User Table
Revision ID: 51e10b2d01ef
Revises: 771f9f24c271
Create Date: 2021-09-27 18:35:28.749279
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '51e10b2d01ef'
down_revision = '771f9f24c271'
branch_labels = None
depends_on = None


def create_user_table():
    """Method that will be called by alembic to create 'User' Table in DB"""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email_verified", sa.Boolean, nullable=False, server_default="False"),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="True"),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default="False"),
        sa.Column("created_on", sa.DateTime),
    )


def upgrade() -> None:
    create_user_table()


def downgrade() -> None:
    op.drop_table("users")
