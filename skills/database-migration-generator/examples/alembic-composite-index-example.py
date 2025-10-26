"""Add composite index on users(email, status) with concurrent build

Revision ID: 9f8e7d6c5b4a
Revises: 1a2b3c4d5e6f
Create Date: 2025-10-26 03:51:54

Zero-downtime migration for PostgreSQL using CONCURRENTLY
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create index concurrently (no table lock)
    op.create_index(
        'idx_users_email_status',
        'users',
        ['email', 'status'],
        postgresql_concurrently=True
    )

def downgrade():
    # Drop index concurrently (safe rollback)
    op.drop_index(
        'idx_users_email_status',
        table_name='users',
        postgresql_concurrently=True
    )
