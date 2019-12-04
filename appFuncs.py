# Damon Adkins -- kk4tza@gmail.com
# 11/27/2019
#
# Functions used to read config file, obtain tokens
# and format strings.
#
# python 3.6
#
# pip install requests and requests_oauthlib
#


import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import re
import json
import time


def getConfig(name):
    """ Reads and returns configuration from file """
    configFile = name + '.json'
    with open(configFile, 'r') as f:
        conf = json.load(f)
    return conf

def saveConfig(name, payload):
    """ Saves config file """
    configFile = name + '.json'
    with open(configFile, 'w') as f:
        json.dump(payload, f, sort_keys=True)

# Authorization Functions #

def authorize(appName):
    """ oAuth2 authorization """
    conf = getConfig(appName)
    oauth = OAuth2Session(client_id=conf['client_id'], redirect_uri=conf['redirect_uri'], scope=conf['scope'])
    authorization_url, state = oauth.authorization_url(conf['auth_service'])
    return authorization_url

def parseAuthCode(url):
    """ Formats auth code from URL """
    reState = re.search('(?<=state=)(.*)', url)
    reAuthCode = re.search('(?<=code=)(.*)(?=&)', url)
    codes = [reAuthCode.group(0), reState.group(0)]
    return codes

def accessToken(conf):
    """ requests access token """
    now = time.time()
    expireTime = now + 180
    oauth = OAuth2Session(client_id=conf['client_id'], redirect_uri=conf['redirect_uri'], scope=conf['scope'])
    getAccessToken = oauth.fetch_token(conf['token_service'], code=conf['auth_code'], client_secret=conf['client_secret'], expires_at=expireTime)
    print('Access Token Issued')
    return getAccessToken

# Access/Refresh token Functions #

def getrefreshToken(conf):
    """ Obtains new refresh token """
    response = requests.post('{}'.format(conf['token_service']),
        data={
        'grant_type': 'refresh_token',
        'refresh_token': conf['refresh_token'],
        'scope': conf['scope']
    },
        auth=HTTPBasicAuth(conf['client_id'], conf['client_secret']))

    if response.status_code != 200:
        code = response.status_code
        return code
    return response.json()


def checkToken(conf):
    """ Checks to see if refresh token
        has expired. Obtains new one. """
    now = time.time()
    expiresIn = int(conf['expires_at']) - int(now)
    if expiresIn < 500:
        newToken = getrefreshToken(conf)
        conf['access_token'] = newToken['access_token']
        conf['refresh_token'] = newToken['refresh_token']
        conf['expires_at'] = now + newToken['expires_in']
        return conf
    else:
        return conf
