import requests
import os

USERNAME = 'N10b1um'
TOKEN = os.environ.get('GH_TOKEN')

events_url = f'https://api.github.com/users/{USERNAME}/events/public'
response = requests.get(events_url)
events = response.json()

last_repo = None
for event in events:
    if event['type'] == 'PushEvent':
        full_repo_name = event['repo']['name']
        last_repo = full_repo_name.split('/')[-1]
        break

if not last_repo:
    print("No recent commits :(")
    exit()

print(f"Last repository: {last_repo}")

graphql_url = 'https://api.github.com/graphql'
headers = {
    'Authorization': f'bearer {TOKEN}',
    'Content-Type': 'application/json'
}

query = """
mutation changeUserStatus($status: ChangeUserStatusInput!) {
  changeUserStatus(input: $status) {
    status {
      message
    }
  }
}
"""

variables = {
    "status": {
        "emoji": ":hammer_and_wrench:",
        "message": f"Working on: {last_repo}"
    }
}

response = requests.post(
    graphql_url, 
    json={'query': query, 'variables': variables}, 
    headers=headers
)

if response.status_code == 200:
    print("Status updated successfully")
else:
    print("Failed to update status: ", response.text)
