from datetime import datetime, timezone
from decimal import Decimal

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


async def get_currency_rate(session: AsyncSession, currency_code: str) -> Decimal:
    """
    Asynchronously retrieves the exchange rate for a given currency code from the database.

    :param session: The SQLAlchemy asynchronous session to use for database queries.
    :type session: AsyncSession
    :param currency_code: The ISO currency code to retrieve the exchange rate for.
    :type currency_code: str
    :return: The exchange rate of the currency.
    :rtype: float
    :raises ValueError: If the currency code is not found in the database.

    Example:
        async with AsyncSession() as session:
            rate = await get_currency_rate(session, 'USD')
            print(f"The exchange rate for USD is {rate}.")
    """
    async with session.begin():
        currency_query = await session.execute(
            select(Currency.rate).where(Currency.code == currency_code)
        )
        currency_rate = currency_query.scalars().first()
        if currency_rate is None:
            raise ValueError(f"Currency {currency_code} is not available.")
        return currency_rate


async def convert_currency(session: AsyncSession, source: str, target: str, amount: float) -> Decimal:
    """
    Converts an amount from one currency to another using their exchange rates.

    :param session: The SQLAlchemy asynchronous session to use for database queries.
    :type session: AsyncSession
    :param source: The ISO code of the source currency.
    :type source: str
    :param target: The ISO code of the target currency.
    :type target: str
    :param amount: The amount in the source currency to be converted.
    :type amount: float
    :return: The amount converted into the target currency.
    :rtype: float
    :raises ValueError: If either the source or target currency code is not found in the database.

    Example:
        async with AsyncSession() as session:
            converted_amount = await convert_currency(session, 'EUR', 'USD', 100)
            print(f"100 EUR is equivalent to {converted_amount} USD.")
    """
    # Get source currency rate
    source_rate = await get_currency_rate(session, source)

    # Get target currency rate
    target_rate = await get_currency_rate(session, target)

    amount_decimal = Decimal(str(amount))

    # Make conversion
    converted_amount = amount_decimal * (target_rate / source_rate)
    return converted_amount


async def get_currencies(session: AsyncSession) -> list:
    """
    Fetches all currencies from the database.

    :param AsyncSession session: The session for database operations.
    :return: A list of Currency objects.
    """
    result = await session.execute(
        select(Currency.rate, Currency.code, Currency.name)
    )
    currencies = result.all()
    return currencies
