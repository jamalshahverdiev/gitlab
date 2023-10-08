import logging
from os import getenv
from re import search
from flask import Flask, request, abort, jsonify
from jira import JIRA

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
SECRET_TOKEN = getenv("SECRET_TOKEN")

def handle_project_create_or_update(data):
    try:
        # Extracting necessary data from payload
        event_name = data.get("event_name")
        user_name = data.get("user_name")
        user_email = data.get("user_email")
        project_name = data.get("project", {}).get("name")
        project_url = data.get("project", {}).get("web_url")
        project_namespace = data.get("project", {}).get("namespace")
        
        # Log extracted data
        logger.info(f"Event: {event_name}, User: {user_name}, Email: {user_email}, Project: {project_name}, Namespace: {project_namespace}, URL: {project_url}")
        
        return jsonify({
            "message": "Project update/create event processed successfully",
            "project_name": project_name,
            "project_namespace": project_namespace
        })
    
    except KeyError as e:
        logger.error(f"Key error: {str(e)}")
        return jsonify({"error": f"Required key not found: {str(e)}"}), 400
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

def handle_merge_request(data):
    author_email = data['user']['email']
    mr_description = data['object_attributes']['description']
    return validate_jira_ticket(mr_description, author_email)

def validate_jira_ticket(mr_description, author_email):
    jira_ticket_regex = r"Closes (\w+-\d+)"
    match = search(jira_ticket_regex, mr_description)
    logger.info(f"Regex match: {match}")
    
    if not match:
        logger.warning("Jira ticket not found in merge request comment.")
        return jsonify({"message": "Merge request has invalid Jira ticket.", "author_email": author_email})
    
    jira_ticket_id = match.group(1)
    logger.info(f"Jira ticket ID: {jira_ticket_id}")
    
    jira_server = getenv('JIRA_SERVER')
    jira_username = getenv('JIRA_USERNAME')
    jira_token = getenv('JIRA_API_TOKEN')
    
    if not all([jira_server, jira_username, jira_token]):
        logger.error("Jira credentials or server URL not set in environment variables.")
        abort(500, description="Jira credentials or server URL not set in environment variables.", response={"author_email": author_email})
    
    jira_options = {'server': jira_server}
    jira = JIRA(options=jira_options, basic_auth=(jira_username, jira_token))
    
    try:
        issue = jira.issue(jira_ticket_id)
        logger.info(f"Issue {jira_ticket_id} exists with summary: {issue.fields.summary}")
    except Exception as e:
        logger.error(f"No issue found with ID {jira_ticket_id} or an error occurred: {str(e)}")
        abort(400, description=f"Ticket defined in the comment is not present in the Jira {jira_server}", response={"author_email": author_email})
    
    return jsonify({"message": "Merge request has a valid Jira ticket.", "author_email": author_email})

@app.route("/webhook", methods=["POST"])
def gitlab_webhook():
    logger.info("Received Webhook call")
    
    request_token = request.headers.get("X-Gitlab-Token")
    if not request_token or request_token != SECRET_TOKEN:
        logger.error("Unauthorized: Invalid secret token.")
        abort(401, description="Unauthorized: Invalid secret token.")
    
    data = request.get_json()
    try:
        object_kind = data.get('object_kind', "")
        event_name = data.get('event_name', "")
        project_namespace = data['project']['namespace']
    except KeyError as e:
        logger.error(f"Error extracting data from payload: {str(e)}")
        abort(400, description="Required data not found in payload.")
    
    # Handling merge request event
    if object_kind == 'merge_request':
        return handle_merge_request(data)

    # Handling project/repository creation/update event
    elif project_namespace == "SRE" and event_name in ['project_create', 'repository_update']:
        return handle_project_create_or_update(data)
    
    # Log and return a message for unhandled event type
    else:
        logger.warning("Unhandled event type")
        return jsonify({"message": "Unhandled event type", "event_name": event_name})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
