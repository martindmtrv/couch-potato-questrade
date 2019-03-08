import requests
from position import Position
from allocation import Allocation
from OAuth2 import AUTH,HEADERS

class Account():
    def __init__(self,api_return):
        # set state from api returns
        self.type = api_return['type']
        self.number = api_return['number']

        # make Position objects for all positions held currently
        self.positions = [Position(x) for x in requests.get(AUTH['api_server'] + 'v1/accounts/' + self.number + '/positions', headers=HEADERS).json()['positions']]

        # get total current cash balance, including market value of all held positions
        balances = requests.get(AUTH['api_server'] + 'v1/accounts/' + self.number + '/balances', headers=HEADERS).json()['combinedBalances'][0]
        self.cash = balances['cash']
        self.equity = balances['marketValue']

        self.allocation = Allocation(self.positions,self.cash+self.equity)
    
    def refresh_balance(self):
        balances = requests.get(AUTH['api_server'] + 'v1/accounts/' + self.number + '/balances', headers=HEADERS).json()['combinedBalances'][0]
        self.cash = float(balances['cash'])
        self.equity = float(balances['marketValue'])
        # returns total equity (cash + equity)
        return self.cash + self.equity
    
    def refresh_positions(self):
        new_data = requests.get(AUTH['api_server'] + 'v1/accounts/' + self.number + '/positions', headers=HEADERS).json()['positions']
        for value,position in enumerate(self.positions,0):
            position = position.refresh_data(new_data[value])
    
    def balancing(self, toMatch):
        capital = self.refresh_balance()
        returnString = ''

        self.refresh_positions()
        # find out how many of each to buy
        for position in toMatch.portion:
            returnString += '\n'
            if type(position) is not str:
                div = toMatch.portion[position] * capital
                orderQuantity = (div // position.currentPrice) - position.openQ
                if orderQuantity > 0:
                    returnString += f'Buy {int(orderQuantity)} shares of {position.symbol}'
                else:
                    returnString += f'Sell {-int(orderQuantity)} shares of {position.symbol}'
            else:
                return returnString



    
    def toString(self):
        return f'{self.type:<6} - {self.number} || Total equity: ${self.refresh_balance():.2f} | Cash: {self.cash:.2f} | Equity: {self.equity:.2f}'