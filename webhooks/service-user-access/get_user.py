from requests import get, put
from os import environ

GITLAB_URL = environ.get('GITLAB_URL', 'http://gitlab.domain.dom')
GITLAB_API = f"{GITLAB_URL}/api/v4"
TOKEN = environ.get('GITLAB_TOKEN', '')
SECRET_TOKEN = environ.get('SECRET_TOKEN', '')
HEADERS = {'PRIVATE-TOKEN': TOKEN}


def print_colored_bold(message, color_code):
    print(f"\033[{color_code}m{message}\033[0m")
    
def get_all_users():
    all_users = []
    page = 1
    per_page = 100

    while True:
        response = get(f'{GITLAB_API}/users', headers=HEADERS, params={'page': page, 'per_page': per_page})
        if response.status_code != 200:
            print(f"Failed to retrieve users: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        all_users.extend(data)

        total_pages = int(response.headers.get('X-Total-Pages', 0))
        if page >= total_pages:
            break

        page += 1

    return all_users

def get_service_accounts(users):
    return [user for user in users if user.get('bot')]

def is_auditor_user(user):
    return user.get('is_auditor', False)

def is_regular_user(user):
    return not (user.get('is_auditor', False) or user.get('is_admin', False))

def set_user_as_auditor(user_id):
    response = put(f'{GITLAB_API}/users/{user_id}?auditor=true&admin=false', headers=HEADERS)
    if response.status_code in [200, 204]:
        print(f"Successfully updated user with ID {user_id}.")
    else:
        print(f"Failed to update user with ID {user_id}: {response.status_code}, {response.text}")

def main():
    users = get_all_users()
    service_accounts = get_service_accounts(users)

    for account in service_accounts:
        if is_auditor_user(account):
            print_colored_bold(f"Auditor Service Account: {account['username']} (ID: {account['id']})", '1;32')
        elif is_regular_user(account):
            print_colored_bold(f"Regular Service Account: {account['username']} (ID: {account['id']})", '1;31')
            set_user_as_auditor(account['id'])
            # if account['username'] == 'some_user_dmkfhsdkjfsdkfs':
            #     print_colored_bold(f"Regular Service Account: {account['username']} (ID: {account['id']})", '1;31')
            #     set_user_as_auditor(account['id'])

if __name__ == "__main__":
    main()
