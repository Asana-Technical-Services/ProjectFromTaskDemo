"""
newRequest/app.py
Lambda Function that handles the workflow to create a new project
"""
import requests
import constants
import utils
import os
import json

def lambda_handler(message, context):

    task_id = message['taskId']
    if task_id is None:
        return
    
    headers = {
                "Authorization": "Bearer " + message['apiKey'],
                "Content-Type": "application/json; charset=utf-8"
            }
    
    # Retrieve task
    task = None
    try:
        url = os.environ['ASANA_API_URL'] + "tasks/" + task_id
        response = requests.get(
            url = url,
            headers = headers,
        )
        print('Get task: {status_code}'.format(status_code=response.status_code))
        response_content = json.loads(response.content)
        task = response_content['data']
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

    if task is  None:
        return
    
    # Write starting comment
    try:
        url = os.environ['ASANA_API_URL'] + "tasks/" + task_id + "/stories"
        response = requests.post(
            url = url,
            headers = headers,
            data = json.dumps({
                "data": {
                    "text": "Starting new project workflow..."
                }
            })
        )
        print('New comment in task: {status_code}'.format(status_code=response.status_code))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')    
    
    # Retrieve metadata
    # ... Title
    task_name = task['name']
    # ... Creation time
    created_at = task['created_at']
    # ... Description
    task_description = task['notes']
    # ... Submitter
    followers = utils.get_follower_gids(task['followers'])
    
    # Duplicate template
    new_project = None
    try:
        url = os.environ['ASANA_API_URL'] + "projects/" + constants.PROJECT_TEMPLATE_GID + "/duplicate"
        response = requests.post(
            url = url,
            headers = headers,
            data = json.dumps({
                "data": {
                    "name": task_name,
                    "include": ["task_notes","task_subtasks","task_attachments","task_dates","task_dependencies"]
                }
            })
        )
        print('Duplicating project template: {status_code}'.format(status_code=response.status_code))
        # print(response.content)
        response_content = json.loads(response.content)
        if response_content['data'] is not None and response_content['data']['new_project'] is not None:
            new_project = response_content['data']['new_project']
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

    if new_project is None:
        print('Could not duplicate the project')
        
    print(new_project)

    
    # Add original task to project
    try:
        url = os.environ['ASANA_API_URL'] + "tasks/" + task_id + "/addProject"
        response = requests.post(
            url = url,
            headers = headers,
            data = json.dumps({
                "data": {
                    "project": new_project['gid'],
                    "insert_after": None
                }
            })
        )
        print('Multi-homing task: {status_code}'.format(status_code=response.status_code))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
    except:
        print("Something HAPPENED!")        
    
    # Add members to new project
    try:
        url = os.environ['ASANA_API_URL'] + "projects/" + new_project['gid'] + "/addMembers"
        response = requests.post(
            url = url,
            headers = headers,
            data = json.dumps({
                "data": {
                    "members": followers,
                }
            })
        )
        print('Adding members to project: {status_code}'.format(status_code=response.status_code))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
    except:
        print("Something HAPPENED!")        
        
    # Write finished comment
    try:
        url = os.environ['ASANA_API_URL'] + "tasks/" + task_id + "/stories"
        response = requests.post(
            url = url,
            headers = headers,
            data = json.dumps({
                "data": {
                    "html_text": "<body> New project created: <a data-asana-gid=\"" + new_project['gid'] + "\"/> </body>"
                }
            })
        )
        print('New comment in task: {status_code}'.format(status_code=response.status_code))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')            