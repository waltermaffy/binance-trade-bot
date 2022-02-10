import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .coin import Coin



class TradeState(enum.Enum):
    STARTING = "STARTING"
    ORDERED = "ORDERED"
    COMPLETE = "COMPLETE"


class Wallet(Base):  # pylint: disable=too-few-public-methods
    __tablename__ = "wallet_history"

    id = Column(Integer, primary_key=True)

    start_holding_id = Column(String, ForeignKey("holdings.symbol"))
    start_holding = relationship("Holding", foreign_keys=[start_holding_id], lazy="joined")
    
    current_holding_id = Column(String, ForeignKey("holdings.symbol"))
    current_holding = relationship("Holding", foreign_keys=[current_holding_id], lazy="joined")
    
    start_datetime = Column(DateTime)
    current_datetime = Column(DateTime)

    alt_starting_balance = Column(Float)
    alt_trade_amount = Column(Float)
    crypto_starting_balance = Column(Float)
    crypto_trade_amount = Column(Float)

    start_value_id = Column(String, ForeignKey("coins.symbol"))
    start_value = relationship("CoinValue", foreign_keys=[start_value_id], lazy="joined")

    current_value_id = Column(String, ForeignKey("coins.symbol"))
    current_value = relationship("CoinValue", foreign_keys=[start_value_id], lazy="joined")


    def __init__(self, holding: Coin, value_coin: Coin):
        self.start_holding = holding
        self.crypto_coin = crypto_coin
        self.state = TradeState.STARTING
        self.selling = selling
        self.datetime = datetime.utcnow()

    def info(self):
        return {
            "id": self.id,
            "alt_coin": self.alt_coin.info(),
            "crypto_coin": self.crypto_coin.info(),
            "selling": self.selling,
            "state": self.state.value,
            "alt_starting_balance": self.alt_starting_balance,
            "alt_trade_amount": self.alt_trade_amount,
            "crypto_starting_balance": self.crypto_starting_balance,
            "crypto_trade_amount": self.crypto_trade_amount,
            "datetime": self.datetime.isoformat(),
        }
