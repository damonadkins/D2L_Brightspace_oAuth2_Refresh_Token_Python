# Damon Adkins - kk4tza@gmail.com
# 11/27/2019
#
# This application will obtain refresh token
# for D2l/Brightspace oAuth 2.0 api applications.
#
# Python 3.6
#
# pip install requests, requests_oauthlib and easygui
#

import requests_oauthlib
from requests_oauthlib import OAuth2Session
import webbrowser
import json
import easygui
from appFuncs import getConfig as getConfig
from appFuncs import saveConfig as saveConfig
from appFuncs import authorize as authorize
from appFuncs import parseAuthCode as parseAuthCode
from appFuncs import accessToken as accessToken

tokenConfigFile = 'tokenConfigTest'

conf = getConfig(tokenConfigFile)
auth = authorize(tokenConfigFile)

webbrowser.open_new_tab(auth)
enterAuthCode = easygui.enterbox('Enter URL from Browser:')

ac = parseAuthCode(enterAuthCode)
conf['auth_code'] = ac[0]
conf['state'] = ac[1]

accToken = accessToken(conf)
print('\n\n' + str(accToken) + '\n\n')
print(conf['auth_code'])

conf['access_token'] = accToken['access_token']
conf['refresh_token'] = accToken['refresh_token']
conf['expires_at'] = accToken['expires_at']
token = {'access_token': conf['access_token'], 'token_type': 'Bearer' }
saveConfig(tokenConfigFile, conf)




