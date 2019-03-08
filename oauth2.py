import requests
import webbrowser

def auth_flow():
    client_id = 'TAmdaaZ2WI35zAIAGCwQWE8uNc_k9A'

    webbrowser.open('https://martindmtrv.github.io/authRedirect.html')
    code = input('Paste code from browser window!\n > ')
    
    return requests.get(f'https://login.questrade.com/oauth2/token?client_id={client_id}&code={code}&grant_type=authorization_code&redirect_uri=https://martindmtrv.github.io/callback.html').json()
    
AUTH = auth_flow()  # get all authorization for app
HEADERS = {'Authorization':AUTH['token_type'] + ' ' + AUTH['access_token']} # set header constant to make calls for entirety of session