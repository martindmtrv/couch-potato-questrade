import requests
import json
from OAuth2 import AUTH,HEADERS
from position import Position
from account import Account
from allocation import Allocation

def main():
    accounts = []
    accounts_call = requests.get(AUTH['api_server']+'v1/accounts',headers=HEADERS).json()
    # find and create all accounts from questrade account
    for account in accounts_call['accounts']:
        accounts.append(Account(account))

    # choose which account to use
    for c,account in enumerate(accounts,1):
        print(f'{c:>4})  {account.toString()}')
    selection = input('Enter account to use\n > ')

    # error check to make sure selection is valid
    while selection not in [str(x) for x in range(1,c+1)]:
        selection = input('Invalid selection\n > ')
    
    currentAccount = accounts[int(selection)-1]
    running = True
    copy = None
    
    while running:
        print('Main menu'.center(80))
        print('\t 1 - Set target allocation\n\t 2 - Calculate portfolio rebalance\n\t 3 - Refresh data\n\t q - quit')
        selection = input('Enter selection\n > ')
        while selection not in ['1','2','3','q']:
            print('Invalid selection')
            selection = input(' > ')
        if selection == '1':
            copy = Allocation(None,None,currentAccount.allocation)
            print(copy.edit())
            
        elif selection == '2':
            if copy is not None:
                print(currentAccount.balancing(copy))
                copy = None
            else:
                print('Set new target allocation first!')
        elif selection == '3':
            currentAccount.refresh_balance()
            print('Refreshed data!')
        else:
            running = False


if __name__ == '__main__':
    main()
