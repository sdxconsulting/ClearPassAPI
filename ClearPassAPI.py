import requests
import json

token_file = 'token.json'
creds_file = 'creds.json'


def getUser():
    # ClearPass - Access Token + Refresh Token
    print("\nImporting Tokens...")
    token_json = readJSON(token_file)
    try:
        access_token = token_json['access_token']
        # refresh_token = token_json['refresh_token']
    except KeyError as error:
        print("ERROR -> Missing key/value pair in", token_file, "->", error)
        exit()
    print("SUCCESS")

    # ClearPass - Base URL + Account Credentials + Client ID/Secret
    print("\nImporting Credentials...")
    creds_json = readJSON(creds_file)
    try:
        base_url = creds_json['base_url']
        grant_type = creds_json['grant_type']
        client_id = creds_json['client_id']
        client_secret = creds_json['client_secret']
        if grant_type != "client_credentials":
            username = creds_json['username']
            password = creds_json['password']
    except KeyError as error:
        if str(error) == "'client_secret'":
            client_secret = input("Client Secret: ")
        elif str(error) == "'username'" or str(error) == "'password'":
            username = input("Username: ")
            password = input("Password: ")
        else:
            print("ERROR -> Missing key/value pair in", creds_file, "->", error)
            exit()
    print("SUCCESS")

    print("\nBase URL: {0}\nClient ID: {1}\nClient Secret: {2}\nGrant Type: {3}\nAccess Token: {4}"
          .format(base_url, client_id, '*' * len(client_secret), grant_type, access_token))

    print("\nVerifying Access Token...")
    api_response = testAccessToken(base_url, access_token)

    if 'status' in api_response:
        print("ERROR -> Invalid Access Token:", api_response['status'], api_response['title'], "->", api_response['detail'])
        print("\nObtaining access token using client credentials...")
        api_response = obtainToken(base_url, client_id, client_secret, grant_type)
        if 'status' not in api_response:
            access_token = api_response['access_token']
            writeJSON('token.json', api_response)
            print("Access Token:", access_token)
        else:
            print("ERROR -> Invalid API Keys:", api_response['status'], api_response['title'], "->", api_response['detail'])
            exit()
    else:
        print("SUCCESS")
    print("\n---------- *** ----------")
    return {
        "base_url": base_url,
        "access_token": access_token
    }


def obtainToken(base_url, client_id, client_secret, grant_type):
    url = base_url + '/oauth'
    payload = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': grant_type}
    response = requests.post(url, data=payload)
    return response.json()


def testAccessToken(base_url, access_token):
    user = {
        "base_url": base_url,
        "access_token": access_token
    }
    return genericQuery(user, "GET", "/cppm-version", {}, {})


def genericQuery(user, method, request_path, parameters, payload):
    url = user['base_url'] + request_path
    headers = {'Content-type': 'application/json', 'Authorization': "Bearer " + user['access_token']}
    if method == "POST":
        response = requests.post(url, headers=headers, params=parameters, data=json.dumps(payload))
    else:
        response = requests.get(url, headers=headers, params=parameters, data=json.dumps(payload))
    return response.json()


def readJSON(file_name):
    try:
        with open(file_name) as file_data:
            return json.load(file_data)
    except IOError as file_error:
        print("ERROR ->", file_name, "->", file_error)
        exit()


def writeJSON(file_name, file_data):
    try:
        with open(file_name, 'w') as outfile:
            return json.dump(file_data, outfile, indent=2)
    except IOError as file_error:
        print("ERROR ->", file_name, "->", file_error)
        exit()
