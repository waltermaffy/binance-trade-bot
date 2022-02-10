"""
Stategia 1. 
Mantieni stabile il numero di coin in holdings accumulando BUSD-BTC in eccesso.

es. 60% btc
    20% eth 
    10% dot 
    05% bnb
    05% ada
    
- BULL PHASE
- LATELARIZATION
- BEAR PHASE

        
1.scegli holdings e ammontare percentuale
 - START_AMOUNT  = 200 BUSD

BUY: 70% BTC , 30% ETH

- calculate first 2 targets coin 

# 2. produci la variazione di prezzo tra tutte le coin

Trova la coin che ha la differenza più grande rispetto al target holdings

Guarda la variazione dei prezzi comulativa

es. Ultimi 60 secondi: 
    BTC ETH DOT
BTC  0  -0.2 0.1
ETH 0.2   0 0.6
DOT 0.1  0.6  0
 
se la variazione è più alta della soglia 
AND
la coin  è target
AND
a profitto


 -- compra ALT alla percentuale del target  
  
"""

import random
import sys
from datetime import datetime
from binance_trade_bot.auto_trader import AutoTrader
from enum import Enum

START_AMOUNT = 200 

class Hold(Enum):
    TARGET = 0
    FIRST = 1
    CURRENT = 2

class StartHolding(Holding):
    
    def __init__(self):

        self.first_holdings = {
                'BTC': 0.70,
                'ETH': 0.30, 
                'DOT': 0,
                'BNB': 0, 
                'ADA': 0,
                'SOL': 0    
            }
        self.start_date = datetime.now()


class Holding():
    def __init__(self, mode=Hold.TARGET):
        
        
        self.start_date = datetime.now()
        if mode == Hold.TARGET:
            self.target_holdings = {
            'BTC': 0.40,
            'ETH': 0.30, 
            'DOT': 0.15,
            'BNB': 0.05, 
            'ADA': 0.05,
            }
        elif mode == Hold.FIRST:
        
        else:
            raise ValueError("Invalid init mode, TARGET or START")

    @classmethod
    def get_start_amount(self):
        return START_AMOUNT
    
    
    def update(self, current_holdings):
        self.holdings = current_holdings

    def get_highest(self, holdings:dict):
        return [(key, value) for key, value in holdings.items() if value == max(holdings.values())][0]


    def add_current_holdings(self, current_holdings: dict):
        self.holdings = current_holdings
    

    def find_target(self):
        """
        Return the coin with with the highest difference between the target 
        """
        targets = {}
        for coin_c, perc_c in self.holdings.items():
            diffs = [(coint_t, abs(perc_c - perc_t)) for coint_t, perc_t 
                     in self.target_holdings.items() if coint_t != coin_c]
            targets[coin_c] = [d for d in diffs if d[1] == min(d[1] for d in diffs)][0]
        return self.get_highest(targets)
    
    
    def add_hold(self, coin, perc):
        self.holdings[coin] = perc
    



def Score(self):
    
    """
    La coin con lo Score più alto sarà scelta come prossimo Target
    """
    def __init__(self):
        self.score = 0


class BalancerStrategy(AutoTrader):
    def initialize(self):
        super().initialize()
        
        """Starting from X USD or X BTC, buy the highest coin that has the highest score
        
        INPUT: 300 USD
        
        Amount always in USD: 50 USDT 
        
        OUTPUT: 100$ BTC 20 the coldest coin 
        
        
        """
        
        #self.initialize_current_coin()
        self.start_holding = StartHolding()
        
        self.initialize_holdings()
     
        
    def initialize_holdings(self):
        
        # tot. 300$ BUY first target
        first_target = self.get_target()
        # BTC 100$ BUY
        
        
        
        self.target_holdings = Holdings('target')
        self.start_holdings = Holdings('start')
        
        # buy first highest target
        self.start_amount = Holdings.get_start_amount()
        first_target = self.start_holdings.get_highest()
        coin_start = first_target[0] # 'BTC'
        coin_start_perc = first_target[1] # '0.7 BTC'
        coin_start_usd = coin_start_perc * self.start_amount 
        self.logger.info(f"{datetime.now()} - CONSOLE - INFO - Buying with {coin_start_perc*100}% of {coin_start}: {coin_start_usd:.2f}")
        # buy coin_start_usd of coin_start
        self.manager.buy(coin_start, coin_start_usd, self.config.BRIDGE)

        # buy second highest target
        #TODO BUY SECOND TARGET
        self.start_amount = Holdings.target_holdings()
        first_target = self.start_holdings.get_highest()
        coin_start = first_target[0] # 'BTC'
        coin_start_perc = first_target[1] # '0.7 BTC'
        coin_start_usd = coin_start_perc * self.start_amount 
        self.logger.info(f"{datetime.now()} - CONSOLE - INFO - Buying with {coin_start_perc*100}% of {coin_start}: {coin_start_usd:.2f}")
        # buy coin_start_usd of coin_start
        self.manager.buy(coin_start, coin_start_usd, self.config.BRIDGE)


    def scout(self):
        
        """
        Scout for potential jumps from the current holdings to different targets
        
        
        hodls = {"BTC: 0.8, "ETH:0.15", ... }
        
        """
        
        # find target coins
        current_holdings = self.db.get_current_holdings()
        target_coin =  current_holdings.find_target()
        
        all_tickers = self.manager.get_all_market_tickers()
        current_coins = self.db.get_current_coins()
        # Display on the console, the current coin+Bridge, so users can see *some* activity and not think the bot has
        # stopped. Not logging though to reduce log size.
        print(
            f"{datetime.now()} - CONSOLE - INFO - I am scouting the buy best coins. "
            f"Target coin: {target_coin + self.config.BRIDGE} ",
            end="\r",
        )

        current_coin_price = all_tickers.get_price(current_coin + self.config.BRIDGE)

        if current_coin_price is None:
            self.logger.info("Skipping scouting... current coin {} not found".format(current_coin + self.config.BRIDGE))
            return

        self._jump_to_best_coin(current_coin, current_coin_price, all_tickers)


    def bridge_scout(self):
        current_coin = self.db.get_current_coin()
        if self.manager.get_currency_balance(current_coin.symbol) > self.manager.get_min_notional(
            current_coin.symbol, self.config.BRIDGE.symbol
        ):
            # Only scout if we don't have enough of the current coin
            return
        new_coin = super().bridge_scout()
        if new_coin is not None:
            self.db.set_current_coin(new_coin)

    def initialize_current_coin(self):
        """
        Decide what is the current coin, and set it up in the DB.
        """
        if self.db.get_current_coin() is None:
            current_coin_symbol = self.config.CURRENT_COIN_SYMBOL
            if not current_coin_symbol:
                current_coin_symbol = random.choice(self.config.SUPPORTED_COIN_LIST)

            self.logger.info(f"Setting initial coin to {current_coin_symbol}")

            if current_coin_symbol not in self.config.SUPPORTED_COIN_LIST:
                sys.exit("***\nERROR!\nSince there is no backup file, a proper coin name must be provided at init\n***")
            self.db.set_current_coin(current_coin_symbol)

            # if we don't have a configuration, we selected a coin at random... Buy it so we can start trading.
            if self.config.CURRENT_COIN_SYMBOL == "":
                current_coin = self.db.get_current_coin()
                self.logger.info(f"Purchasing {current_coin} to begin trading")
                all_tickers = self.manager.get_all_market_tickers()
                self.manager.buy_alt(current_coin, self.config.BRIDGE, all_tickers)
                self.logger.info("Ready to start trading")
