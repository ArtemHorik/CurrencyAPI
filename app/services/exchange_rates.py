import httpx

from app.utils.logger import logger


async def fetch_current_exchange_rates(api_key: str) -> dict:
    """
    Asynchronously fetches the current exchange rates using the ExchangeRatesAPI (EUR base).

    :param api_key: The API key for accessing the ExchangeRatesAPI.
    :type api_key: str
    :return: A dictionary with currency exchange rates.
    :rtype: dict
    :raises HTTPStatusError: If the request to the API ends with an error.

    This function makes a GET request to the ExchangeRatesAPI to obtain the current exchange rates and returns them
    as a dictionary. If an error occurs during the request (e.g., incorrect API key or problems accessing the
    service), an HTTPStatusError exception is raised.
    """
    url = f"http://api.exchangeratesapi.io/latest?access_key={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        try:
            data = response.json()
            return data['rates']
        except KeyError as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
            raise ValueError(f"The response from the API does not contain 'rates'. Response was: {response.text}")

