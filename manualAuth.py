import requests
import json

def auth_flow():
    # store refresh id
    try:
        with open('auth.json','r') as f:
            line = f.read().rstrip()
            auth_dict = json.loads(line)
    except FileNotFoundError:
        auth_dict = {'refresh_token':'4q07HZBPPJa6AHfdI512hTphgugb61DC0'}

    # webbrowser open to open homepage
    auth_dict = requests.get('https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token='+auth_dict['refresh_token']).json()

    # save new auth credentials
    with open('auth.json', 'w') as f:
        f.write(str(auth_dict).replace("\'", "\"")) # replace ' with " for json storing
    
    return auth_dict

# define these in global scope
AUTH = auth_flow()  # get all authorization for app
HEADERS = {'Authorization':AUTH['token_type'] + ' ' + AUTH['access_token']} # set header constant to make calls for entirety of session