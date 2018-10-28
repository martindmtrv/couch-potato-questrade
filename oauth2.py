import requests
import json
import webbrowser
import os

def auth_flow():
    # oauth2 authentication flow
    client_id = 'Esw5KFjjfgBJAAlB3YIs2NlDG6sz2Q'

    # open browser and get login
    webbrowser.open('https://practicelogin.questrade.com/oauth2/authorize?client_id='+ client_id +'&response_type=code&redirect_uri=https://martindmtrv.github.io/redirect.html')

    # wait for user to input response code (from browser redirect)
    client_secret = input('Paste redirect code from browser (string after ?code=)\n > ')
    auth_response = requests.get('https://practicelogin.questrade.com/oauth2/token?client_id="' + client_id + '"&code=' + client_secret + '&grant_type=authorization_code&redirect_uri=https://martindmtrv.github.io/redirect.html')

    # build auth header dictionary and return
    print(auth_response.content)
    auth_dict = json.loads(auth_response.content.decode('utf-8'))
    return auth_dict

def select_account(headers,response_token):

    # make account get request
    accounts_list = json.loads(requests.get(response_token['api_server']+'v1/accounts', headers=headers).content.decode('utf-8'))

    # print all available accounts
    print('Select an account to rebalance:')
    for number, account_types in enumerate(accounts_list['accounts'], 1):
        print('\t{}) {} - {}'.format(number,account_types['type'],account_types['number']))

    # ask user to select an account, and error check
    selection = input(' > ')
    accounts_range = [str(x) for x in list(range(1,len(accounts_list['accounts'])+1))]
    while not selection in accounts_range:
        print('Invalid Selection!')
        selection = input(' > ')

    return accounts_list['accounts'][int(selection)]

def current_positions(headers,response_token,account):
    # get request to see current positions with given account
    positions_list = json.loads(requests.get(response_token['api_server']+'v1/accounts/'+account['number']+'/positions',headers=headers,params={'id': account['number']}).content.decode('utf-8'))

    print(positions_list)

def order_history(headers,response_token,account):
    order_list = json.loads(requests.get(response_token['api_server']+'v1/accounts/'+account['number']+'/orders',headers=headers).content.decode('utf-8'))

    print(order_list)

def search_securities(headers,response_token):
    prefix = input('Enter a symbol to search:\n > ')
    search_results = json.loads(requests.get(response_token['api_server']+'v1/symbols/search',headers=headers,params={'prefix':prefix}).content.decode('utf-8'))
    print(search_results)

def balances(headers,response_token,account):
    balance_list = json.loads(requests.get(response_token['api_server']+'v1/accounts/'+account['number']+'/balances',headers=headers,params={'id':account['number']}).content.decode('utf-8'))

    print(balance_list)


response_token = auth_flow()
headers = {'Authorization': response_token['token_type'] + ' ' + response_token['access_token']}
account = select_account(headers,response_token)

running = True

while running:
    os.system('cls')
    print('Main Menu'.center(80))
    choice = input('Choose an option:\n\t 1) Search Securities\n\t 2) Check current holdings\n\t 3) Check order history\n\t 4) Check balances\n\t q - Quit\n > ')
    options = [str(x) for x in list(range(1,5))]
    options.append('q')
    while not choice in options:
        choice = input('Invalid Selection\n > ')
    if choice == '1':
        securities = search_securities(headers,response_token)
        input('..')
    elif choice == '2':
        positions = current_positions(headers,response_token,account)
        input('..')
    elif choice == '3':
        orders = order_history(headers,response_token,account)
        input('..')
    elif choice == '4':
        money = balances(headers,response_token,account)
        input('..')
    else:
        running = False
