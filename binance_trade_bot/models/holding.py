from sqlalchemy import Boolean, Column, String

from .base import Base


class Holding(Base):
    __tablename__ = "holdings"
    
    # list of coins
    # usd_value 
    # datetime 
    id_ = Column(String, primary_key=True)
    coin_value_id = Column(String, primary_key=True)
    usd_value = Column(String)
    datetime = Column(String)
    
    def __init__(self, coin_value, usd_value, datetime):
        self.id_ = coin_value.id_
        self.coin_value_id = coin_value.id_
        self.usd_value = usd_value
        self.datetime = datetime    

    

    def __init__(self, symbol, enabled=True):
        self.symbol = symbol
        self.enabled = enabled

    def __add__(self, other):
        if isinstance(other, str):
            return self.symbol + other
        if isinstance(other, Coin):
            return self.symbol + other.symbol
        raise TypeError(f"unsupported operand type(s) for +: 'Coin' and '{type(other)}'")

    def __repr__(self):
        return f"<{self.symbol}>"

    def info(self):
        return {"symbol": self.symbol, "enabled": self.enabled}
