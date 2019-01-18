import ClearPassAPI

# CONFIRM OR CREATE VALID USER FOR SUBSEQUENT API CALLS
user = ClearPassAPI.getUser()

# SAMPLE USE CASE -> List of Active Guest Accounts
params = {"calculate_count": "true", "filter": '{"current_state": "active"}'}
guest = ClearPassAPI.genericQuery(user, 'GET', '/guest', params, {})
print("\nACTIVE GUEST ACCOUNTS (" + str(guest['count']) + ")")
if guest['count'] > 0:
    for item in guest['_embedded']['items']:
        if 'username' in item:
            print(item['visitor_name'], "->", item['username'])
else:
    print("There are no active guests.")
