from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Config
from app.db.currency_operations import get_last_update_time, update_exchange_rates, convert_currency, get_currencies
from app.db.engine import get_session
from app.db.models.currency import Currency
from app.services.exchange_rates import fetch_current_exchange_rates
from app.utils.logger import logger

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    logger.info("Starting up the application...")


@app.get("/currencies")
async def read_currencies(session: AsyncSession = Depends(get_session)):
    """
    Endpoint to read all available currencies from the database.

    :param AsyncSession session: Dependency injection of the database session for performing asynchronous DB operations.
    :return: JSON list of all currencies.
    """
    currencies = await get_currencies(session)
    return currencies


@app.get("/last-update-time")
async def read_last_update_time(session: AsyncSession = Depends(get_session)):
    """
    Retrieves the last time the exchange rates were updated in the database.

    :param AsyncSession session: Dependency injection of the database session for performing asynchronous DB operations.
    :return: JSON response containing the last update time in 'dd-MMM-yyyy HH:mm' format if found.
    :rtype: dict
    :raises HTTPException: 404 error if last update time not found.
    """
    last_update_time = await get_last_update_time(session)
    if last_update_time:
        return {"last_update_time": last_update_time.strftime("%d-%b-%Y %H:%M")}
    else:
        raise HTTPException(status_code=404, detail="Last update time not found.")


@app.post("/update-rates")
async def update_rates(session: AsyncSession = Depends(get_session)):
    """
    Endpoint to update exchange rates in the database with current rates from an external API.

    :param AsyncSession session: Dependency injection of the database session for performing asynchronous DB operations.
    :return: JSON response with a success message if the rates are updated successfully.
    :rtype: dict
    :raises HTTPException: 500 error with detail of the exception in case of failure during rates update.
    """
    try:
        # Get new rates
        rates = await fetch_current_exchange_rates(Config.API_KEY)
        # Update existing rates in db
        await update_exchange_rates(session, rates)
        return {"message": "Exchange rates updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@app.get("/convert")
async def convert_endpoint(source: str, target: str, amount: float, session: AsyncSession = Depends(get_session)):
    """
    Converts a specified amount from a source currency to a target currency using the latest exchange rates.

    :param str source: The ISO currency code for the source currency.
    :param str target: The ISO currency code for the target currency.
    :param float amount: The amount of the source currency to convert.
    :param AsyncSession session: Dependency injection of the database session for performing asynchronous DB operations.
    :return: JSON response containing the converted amount if the conversion is successful.
    :rtype: dict
    :raises HTTPException: 400 error with detail of the exception if conversion cannot be performed.
    """
    try:
        result = await convert_currency(session, source, target, amount)
        return {"converted_amount": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
