import requests
import sys
import json
import time

AUTHCODE = sys.argv[1]
CLIENTID = "YOUR CLIENT ID"
REDIRECT = "https://localhost"
SECRET = "YOUR SECRET"

print('Given the authentication token, retrieve the oauth pair (access token and refresh token)')
r = requests.post("https://test-api.service.hmrc.gov.uk/oauth/token", data={'client_secret': SECRET, 'client_id': CLIENTID, 'grant_type': 'authorization_code', 'redirect_uri': REDIRECT, 'code': AUTHCODE})
code = r.status_code
if ( r.status_code != 200):
	print('Boo.  Somthing failed - here\'s the reason:')
	print(r.status_code, r.reason)
	print(r.text)
	print('Try getting the authorisation token again:')
	print('https://test-api.service.hmrc.gov.uk/oauth/authorize?response_type=code&client_id='+CLIENTID+'&scope=hello&redirect_uri='+REDIRECT )
	sys.exit()
else:
	print('Yay!  We now have an oauth pair.')
	data = json.loads(r.text)
	accessToken = data['access_token']
	refreshToken = data['refresh_token']
	print('Access Token = '+accessToken)
	print('Refresh Token = '+refreshToken)

	print('Now time to call the API using the access token.')
	while True:
		hello = requests.get("https://test-api.service.hmrc.gov.uk/hello/user", headers={"Accept": "application/vnd.hmrc.1.0+json", "Authorization": "Bearer "+accessToken})

		if ( hello.status_code != 200):
			print('Pants!  Something went wrong:'+r.reason)
			print(r.text)
			sys.exit()
		else:		
			print('API says.... '+hello.text)
			print('OK, lets pretend that we have been calling the API for a few hours...')
			print('Now it\'s time to refresh the access token because it will stop working after 4 hours')

			r = requests.post("https://test-api.service.hmrc.gov.uk/oauth/token", data={'client_secret': SECRET, 'client_id': CLIENTID, 'grant_type': 'refresh_token', 'redirect_uri': REDIRECT, 'refresh_token': refreshToken})
			code = r.status_code
			if ( r.status_code != 200):
				print('Double boo.  Unable to refresh the token - here\'s the reason:')
				print(r.status_code, r.reason)
				print(r.text)
				print('Try getting the authorisation token again:')
				print('https://test-api.service.hmrc.gov.uk/oauth/authorize?response_type=code&client_id='+CLIENTID+'&scope=hello&redirect_uri='+REDIRECT )
				sys.exit()
			else:
				print('Super. Consider it refreshed.')
				data = json.loads(r.text)
				accessToken = data['access_token']
				refreshToken = data['refresh_token']
				print('Access Token = '+accessToken)
				print('Refresh Token = '+refreshToken)

				print('Wait for a moment so that we don\'t have a zillion messages printed....')
				time.sleep(5) 

				print('Trying the API with the new access token....')
