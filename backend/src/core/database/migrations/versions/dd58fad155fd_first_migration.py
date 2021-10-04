# this file will instruct alembic how to generate new migration scripts

"""create_todos_main_table
Revision ID: 54e4ed17d063
Revises: 
Create Date: 2021-08-15 18:33:21.312153
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '54e4ed17d063'
down_revision = None
branch_labels = None
depends_on = None


def create_todos_table():
    """method that will create "TODOItem" table """
    op.create_table(
        "todos",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("text", sa.String(150)),
        sa.Column("owner_id", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(('owner_id',), ['users.id'], ),
        sa.Column("completed", sa.Boolean, nullable=False),
        sa.Column("created_on", sa.DateTime),
    )


def upgrade() -> None:
    create_todos_table()


def downgrade() -> None:
    op.drop_table("todos")
