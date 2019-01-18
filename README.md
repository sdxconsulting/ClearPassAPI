# ClearPassAPI
Python code to interface with the Aruba ClearPass APIs (including OATH token management)

## Getting Started
These instructions will assist get the project up and running on your local machine for development and testing purposes.

### Prerequisites
* An active ClearPass platform and an API Client defined in the ClearPass Admin UI at "Guest -> Administration -> API Services -> API Clients".
* Configure the "Grant Type" as "Client credentials" and take note of the "Client ID" and "Client Secret" associated with your API client.
* It is recommended that the API client has a "Read-only Administrator" operator profile if you do not wish for your environment to be modified.

### Installing
Deploy all files into a new project using your preferred Python IDE, and modify "token.json" and "creds.json" as below before running "ClearPassLab.py" for the first time:

#### *token.json*
```
{
  "access_token": "can_be_blank_if_no_valid_token_exists",
  "token_type": "Bearer"
}
```
Note that *token.json* will be automatically updated with the most recent access and refresh token/s if either are generated or refreshed through the OATH workflow.

#### *creds.json*
```
{
  "base_url": "https://YOUR_CPPM_PLATFORM/api",
  "grant_type": "client_credentials",
  "client_id": "Client_ID_as_defined_in_prerequisities",
  "client_secret": "Client_Secret_as_defined_in_prerequisities"
}
```

## Running
There are sample use cases in *ClearPassLab.py* to demonstrate how to use *ClearPassAPI.py*.

The high-level process is to first instantiate a user which will ensure that a valid access token exists:
```
user = ClearPassAPI.getUser()
```

If both *token.json* and *creds.json* are accessible and have all required key/value pairs:
```
Importing Tokens...
SUCCESS

Importing Credentials...
SUCCESS
```

If any key/value pairs are missing from either *token.json* and/or *creds.json*:
```
Importing Tokens...
ERROR -> Missing key/value pair in token.json -> 'access_token'

Importing Credentials...
ERROR -> Missing key/value pair in creds.json -> 'base_url'
```

If *token.json* contains a valid "access_token":
```
Verifying Access Token...
SUCCESS
```

If *token.json* contains an invalid "access_token" AND *creds.json* contains invalid API client credentials:
```
Verifying Access Token...
ERROR -> Invalid Access Token: 403 Forbidden -> Access denied

Obtaining access token using client credentials...
ERROR -> Invalid API Keys: 400 invalid_client -> The client credentials are invalid
```

If *token.json* contains an invalid "access_token" BUT *creds.json* contains valid API client credentials:
```
Verifying Access Token...
ERROR -> Invalid Access Token: 403 Forbidden -> Access denied

Obtaining access token using client credentials...
Access Token: ****************************************
```

Once a valid user has been instantiated, a generic GET query can be made by providing the specific URL suffix for the API call that is required and passing the appropriate parameters and/or payload.  For example, to return all active Guest users:
```
request_path = "/guest"
parameters = {
    "calculate_count": "true",
    "filter": '{"current_state": "active"}'
}
payload = {}

api_response = ClearPassAPI.genericQuery(user, 'GET', request_path, parameters, payload)
```

Similarly, a generic POST query can be made by providing the specific URL suffix for the API call that is required and passing the appropriate parameters and/or payload.  For example, to create a new device in the Guest database:
```
request_path = "/device"
parameters = {"change_of_authorization": "true"}
payload = {
    "visitor_name": "Random_Device",
    "mac": "012345678900",
    "role_name": "Registered Device",
    "role_id": 4,
    "enabled": "true"
}

api_response = ClearPassAPI.genericQuery(user, 'POST', request_path, parameters, payload)
```

## Contributing
I am open to requests to update, modify and improve this code!  Please let me know if you have feedback or would like to contribute and we can discuss options to do so.

## Versioning
* *v1.0 (January 2019)* - **Nick Harders** @ [NicholasHarders](https://github.hpe.com/nicholas-harders)
