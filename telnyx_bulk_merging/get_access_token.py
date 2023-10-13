import requests
import json

#use the Marketo REST API token endpoint to obtain an access token and the
#lifespan of the token in seconds
#https://developers.marketo.com/rest-api/authentication/#creating_an_access_token
def getToken ():
    response = requests.get('https://xxx-xxx-xxx.mktorest.com/identity/oauth/token?grant_type=client_credentials&client_id=xxxx&client_secret=xxx')

    dictionary = json.loads(response.text)

    token = dictionary['access_token']
    expires = dictionary['expires_in']

    return [token, expires]
