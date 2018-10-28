import requests
import json
import webbrowser
import os
import PySimpleGUI as sg

def auth_flow():
    # oauth2 authentication flow
    client_id = 'Esw5KFjjfgBJAAlB3YIs2NlDG6sz2Q'

    # open browser and get login
    webbrowser.open('https://practicelogin.questrade.com/oauth2/authorize?client_id='+ client_id +'&response_type=code&redirect_uri=https://martindmtrv.github.io/redirect.html')

    # wait for user to input response code (from browser redirect)
    layout = [  [sg.Text('Paste redirect code from browser (string after ?code=)')],
                [sg.InputText(key='__key__')],
                [sg.Ok()]]

    # open popup window
    window = sg.Window('Redirect Code').Layout(layout)
    # read window events
    event, client_secret = window.Read()

    # if 'x' pressed quit the program
    if event == None:
        return None, False

    # check if input is blank
    while client_secret['__key__'] == '':
        sg.Popup('Code cannot be blank')
        event, client_secret = window.Read()
        if event == None:
            return None, False

    # close popup and retrieve value from dictionary
    window.Close()
    client_secret = client_secret['__key__']

    # send auth request to questrade
    auth_response = requests.get('https://practicelogin.questrade.com/oauth2/token?client_id="' + client_id + '"&code=' + client_secret + '&grant_type=authorization_code&redirect_uri=https://martindmtrv.github.io/redirect.html')

    # build auth header dictionary and return
    auth_dict = json.loads(auth_response.content.decode('utf-8'))
    return auth_dict, True

def select_account(headers,response_token):
    # make account get request
    accounts_list = json.loads(requests.get(response_token['api_server']+'v1/accounts', headers=headers).content.decode('utf-8'))

    account_types = [x['type'] + ' - ' + x['number'] for x in accounts_list['accounts']]
    # print all available accounts
    layout = [[sg.Text('Account selection')],
              [sg.Listbox(values=account_types, size=(30, 6))],
              [sg.Ok()]
    ]
    window = sg.Window('Select account from list below').Layout(layout)
    event, account = window.Read()
    if event is None:
        window.Close()
        return None, False
    while account[0] == []:
        sg.Popup('Choose an account!')
        event, account = window.Read()
    window.Close()
    return account[0][0][account[0][0].index('-')+2:],True

def current_positions(headers,response_token,accountNum):
    # get request to see current positions with given account
    positions_list = json.loads(requests.get(response_token['api_server']+'v1/accounts/'+accountNum+'/positions',headers=headers,params={'id': accountNum}).content.decode('utf-8'))

    print(positions_list)

def order_history(headers,response_token,accountNum):
    order_list = json.loads(requests.get(response_token['api_server']+'v1/accounts/'+accountNum+'/orders',headers=headers).content.decode('utf-8'))

    print(order_list)

def search_securities(headers,response_token):
    prefix = input('Enter a symbol to search:\n > ')
    search_results = json.loads(requests.get(response_token['api_server']+'v1/symbols/search',headers=headers,params={'prefix':prefix}).content.decode('utf-8'))
    print(search_results)

def balances(headers,response_token,accountNum):
    balance_list = json.loads(requests.get(response_token['api_server']+'v1/accounts/'+accountNum+'/balances',headers=headers,params={'id':accountNum}).content.decode('utf-8'))

    print(balance_list)


response_token, running = auth_flow()

if running:
    headers = {'Authorization': response_token['token_type'] + ' ' + response_token['access_token']}
    accountNum, running = select_account(headers,response_token)

while running:
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
        positions = current_positions(headers,response_token,accountNum)
        input('..')
    elif choice == '3':
        orders = order_history(headers,response_token,accountNum)
        input('..')
    elif choice == '4':
        money = balances(headers,response_token,accountNum)
        input('..')
    else:
        running = False
