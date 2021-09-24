# this file will instruct alembic how to generate new migration scripts

"""Create new Comment table
Revision ID: 771f9f24c271
Revises: 54e4ed17d063
Create Date: 2021-09-17 04:55:54.854794
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '771f9f24c271'
down_revision = '54e4ed17d063'
branch_labels = None
depends_on = None


def create_comments_table(): 

    """method that will create "Comments" table """ 

    op.create_table( 

        "comments", 

        sa.Column("id", sa.Integer, primary_key=True, index=True), 

        sa.Column("text", sa.String(150)), 

        sa.Column("todo_id", sa.Integer, sa.ForeignKey("todos.id")), 

        sa.Column("created_on", sa.DateTime), 

    ) 

def upgrade() -> None:
    create_comments_table()

def downgrade() -> None:
    op.drop_table("comments")


