from decimal import Decimal

import pytest
from unittest.mock import patch

from app.db.currency_operations import convert_currency


@pytest.mark.asyncio
@patch('app.db.currency_operations.get_currency_rate')
async def test_convert_currency(mock_get_currency_rate):
    mock_get_currency_rate.side_effect = [Decimal('1.2'),
                                          Decimal('0.8')]

    converted_amount = await convert_currency(None, 'USD', 'EUR', 100)

    expected_amount = Decimal('100') * (Decimal('0.8') / Decimal('1.2'))
    assert converted_amount == expected_amount, "The converted amount does not match the expected value."
