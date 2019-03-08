import requests
from OAuth2 import AUTH,HEADERS

class Position():
    def __init__(self,api_return):
        # set state from api returns
        self.symbol = api_return['symbol']
        self.id = api_return['symbolId']
        self.currentPrice = api_return['currentPrice']
        self.openQ = api_return['openQuantity']
   
    def refresh_data(self,api_return):
        self.currentPrice = api_return['currentPrice']
        self.openQ = api_return['openQuantity']

    def open_value(self):
        return self.currentPrice * self.openQ
    
    def toString(self):
        # make some readable string
        return f'{self.symbol} - Current Price: ${self.currentPrice:.2f} Open Quantity: {self.openQ}'