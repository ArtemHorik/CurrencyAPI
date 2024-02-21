from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.currency_operations import get_last_update_time
from app.db.engine import get_session
from app.db.models.currency import Currency

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    pass


@app.get("/ping")
async def ping():
    return {"ping": "pong!"}


@app.get("/currencies")
async def read_currencies(session: AsyncSession = Depends(get_session)):
    async with session.begin():
        result = await session.execute(select(Currency))
        currencies = result.scalars().all()
    return currencies


@app.get("/last-update-time")
async def read_last_update_time(session: AsyncSession = Depends(get_session)):
    last_update_time = await get_last_update_time(session)
    if last_update_time:
        return {"last_update_time": last_update_time}
    else:
        raise HTTPException(status_code=404, detail="Last update time not found.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
