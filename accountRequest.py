import requests
import json

class account:
    def __init__(self):
        try:
            # try to authenticate using previous headers
            with open('saveAuth','rb') as readAuth:
                stringByte = readAuth.readline().decode('utf-8')
                auth = json.loads(stringByte)
                self.headers = {'Authorization': auth['token_type'] + ' ' + auth['access_token']}
        except:
            # if no previous authentication exists ask for refresh token and request headers from api
            # save the headers into a file for reuse
            auth = requests.get('https://practicelogin.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token=bmxnuW7eZ2ldPkc_rURDMM56BenvABBL0')
            with open('saveAuth','wb') as saveAuth:
                saveAuth.write(auth.content)
            auth = json.loads(auth.content.decode('utf-8'))
            self.headers = {'Authorization': auth['token_type'] + ' ' + auth['access_token']}

    def get_accounts(self):
        self.accounts = requests.get('https://api04.iq.questrade.com/v1/accounts',headers=self.headers)
        self.accounts = json.loads(self.accounts.content.decode('utf-8'))
        print(type(self.accounts),self.accounts)
        for details in self.accounts['accounts']:
            print(details['type'],details['number'])
martin = account()
martin.get_accounts()
