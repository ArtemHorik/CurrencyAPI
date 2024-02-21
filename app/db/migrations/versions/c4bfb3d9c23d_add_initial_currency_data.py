"""Add initial currency data

Revision ID: c4bfb3d9c23d
Revises: cb079d9bc963
Create Date: 2024-02-20 22:18:27.165885

"""

from alembic import op
from sqlalchemy import table, column, String, Float, DateTime

from app.db.migrations.initial_currencies import initial_currencies, last_update_time

# revision identifiers, used by Alembic.
revision = 'c4bfb3d9c23d'
down_revision = 'cb079d9bc963'
branch_labels = None
depends_on = None


def upgrade() -> None:
    currencies_table = table('currencies',
                             column('name', String),
                             column('code', String),
                             column('rate', Float),
                             )

    op.bulk_insert(currencies_table, initial_currencies)

    currency_updates_table = table('currency_updates',
                                   column('last_updated', DateTime),
                                   )
    op.bulk_insert(currency_updates_table, [{'last_updated': last_update_time}])

def downgrade() -> None:
    op.execute("DELETE FROM currencies")
    op.execute("DELETE FROM currency_updates")
