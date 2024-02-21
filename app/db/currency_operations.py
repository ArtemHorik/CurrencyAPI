from datetime import datetime, timezone

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.currency import CurrencyUpdate, Currency


async def get_last_update_time(session: AsyncSession) -> datetime:
    """
    Asynchronously retrieves the last update time of the exchange rates in the database.

    :param session: The SQLAlchemy async session to execute database operations.
    :type session: AsyncSession
    :return: The timestamp of the last update or None if no updates are found.
    :rtype: datetime or None

    This function executes a query to find the most recent update record in the CurrencyUpdate table,
    ordering by the `last_updated` field in descending order and returning the latest update time.
    If no records are found, it returns None.
    """
    async with session.begin():
        query = select(CurrencyUpdate).order_by(CurrencyUpdate.last_updated.desc()).limit(1)
        result = await session.execute(query)
        last_update = result.scalars().first()
        return last_update.last_updated if last_update else None


async def update_exchange_rates(session: AsyncSession, rates: dict) -> None:
    """
    Asynchronously updates exchange rates in the database with the provided rates,
    and records the time of the update.

    :param session: The SQLAlchemy async session to execute database operations.
    :type session: AsyncSession
    :param rates: A dictionary of currency codes to their respective new exchange rates.
    :type rates: dict
    :return: None

    For each currency code in the `rates` dictionary, this function updates the corresponding record
    in the Currency table with the new rate. It then adds a new record to the CurrencyUpdate table
    to log the time of the update. This operation is performed within a transaction.
    """
    async with session.begin():
        # Update currencies rates
        for code, rate in rates.items():
            await session.execute(
                update(Currency).
                where(Currency.code == code).
                values(rate=rate)
            )

        # Add last update record
        last_update_record = CurrencyUpdate(last_updated=datetime.now(timezone.utc))
        session.add(last_update_record)
        await session.commit()
