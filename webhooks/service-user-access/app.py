from flask import Flask, request
from requests import put, get
from os import environ
from logging import basicConfig, DEBUG, info, warning, error

app = Flask(__name__)
basicConfig(level=DEBUG)

GITLAB_URL = environ.get('GITLAB_URL', 'https://gitlab.domain.dom')
TOKEN = environ.get('GITLAB_TOKEN', '')
SECRET_TOKEN = environ.get('SECRET_TOKEN', '')
HEADERS = {'PRIVATE-TOKEN': TOKEN}

def get_user_details(username):
    response = get(f'{GITLAB_URL}/api/v4/users?username={username}', headers=HEADERS)
    if response.status_code == 200:
        users = response.json()
        if users:
            return users[0]  
    else:
        error(f"Failed to get user details for username {username}: {response.status_code}, {response.text}")
    return None

def set_user_as_auditor(user_id):
    response = put(f'{GITLAB_URL}/api/v4/users/{user_id}?auditor=true&admin=false', headers=HEADERS)
    if response.status_code in [200, 204]:
        info(f"Successfully updated user with ID {user_id}.")
    else:
        error(f"Failed to update user with ID {user_id}: {response.status_code}, {response.text}")

@app.route('/', methods=['GET'])
def index():
    token = request.headers.get('X-Secret-Token')

    if token == SECRET_TOKEN:
        return "Token verified successfully", 200
    else:
        return "Invalid token", 403

@app.route('/gitlab-webhook', methods=['POST'])
def gitlab_webhook():
    info("Received a request: %s", request.data.decode("utf-8"))

    if request.headers.get('X-Gitlab-Token') != SECRET_TOKEN:
        warning("Invalid secret token received.")
        return 'Invalid secret token', 403

    data = request.json

    if data and data.get('event_name') == 'user_create':
        info("Processing user_create event")
        user_id = data.get('user_id')
        username = data.get('username')
        user_details = get_user_details(username)
        
        if user_details:
            user_is_bot = user_details.get('bot', False)
            user_is_admin = user_details.get('is_admin', False)
            user_is_auditor = user_details.get('is_auditor', False)

            if user_is_bot and not user_is_admin and not user_is_auditor:
                info(f"Updating user ID {user_id} to auditor.")
                set_user_as_auditor(user_id)
            else:
                info(f"No action required for user ID {user_id}.")

    return '', 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
