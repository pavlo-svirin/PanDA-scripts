import globus_sdk
from pprint import pprint

CLIENT_ID = '142f3677-a8d5-4988-9d74-dec388f89229'

client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
#client.oauth2_start_flow()

#authorize_url = client.oauth2_get_authorize_url()
#print('Please go to this URL and login: {0}'.format(authorize_url))

# this is to work on Python2 and Python3 -- you can just use raw_input() or
# input() for your specific version
#get_input = getattr(__builtins__, 'raw_input', input)
#auth_code = get_input(
#    'Please enter the code you get after login here: ').strip()
#token_response = client.oauth2_exchange_code_for_tokens(auth_code)

#globus_auth_data = token_response.by_resource_server['auth.globus.org']
#globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']

# most specifically, you want these tokens as strings
AUTH_TOKEN = 'AgMQwzbXak3qjGrrwMkkDb2WdGG6gX4bMelw0q0n47JrBQwbdrHOCQoE0d8mzGP9Meky0BQyGemXmxTvaqpJkirG9jTKmqEueYWD'
TRANSFER_TOKEN = 'Ag46bJE80mgJdqyQldlXnOv2E686xJ8rVpN1aKggl0k66QJbBQu7CxKBQPwoX0V2X7GejDqoaD4xKwujvpYq9hV4BN'

print AUTH_TOKEN
print TRANSFER_TOKEN




# a GlobusAuthorizer is an auxiliary object we use to wrap the token. In
# more advanced scenarios, other types of GlobusAuthorizers give us
# expressive power
authorizer = globus_sdk.AccessTokenAuthorizer(TRANSFER_TOKEN)
tc = globus_sdk.TransferClient(authorizer=authorizer)

# high level interface; provides iterators for list responses
print("My Endpoints:")
for ep in tc.endpoint_search(filter_scope="my-endpoints"):
    print("[{}] {}".format(ep["id"], ep["display_name"]))
