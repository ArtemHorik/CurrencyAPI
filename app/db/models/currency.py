from sqlalchemy import Column, Integer, String, Float, func, DateTime
from app.db.models import BaseModel


class Currency(BaseModel):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    rate = Column(Float)


class CurrencyUpdate(BaseModel):
    __tablename__ = 'currency_updates'

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
