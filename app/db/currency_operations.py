from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.currency import CurrencyUpdate


async def get_last_update_time(session: AsyncSession) -> datetime:
    async with session.begin():
        query = select(CurrencyUpdate).order_by(CurrencyUpdate.last_updated.desc()).limit(1)
        result = await session.execute(query)
        last_update = result.scalars().first()
        return last_update.last_updated if last_update else None
