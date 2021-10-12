"""
bot/app.py
Lambda Function that reviews the events received from Asana and routes
to the appropriate workflow
"""
import os
import json
import boto3
import secrets

section_gid = "1200934971198988"

bot_state_machine_arn = os.environ['BOT_STATE_MACHINE_ARN']
client = boto3.client('stepfunctions')


def lambda_handler(event, context):

    # Init
    secret = None
    signature = None
    event_headers = event['headers']

    # Retrieve secret or signature
    try:
        secret = event_headers['X-Hook-Secret']
    except:
        print('x-hook-secret does not exist')

    try:
        signature = event_headers['X-Hook-Signature']
    except:
        print('x-hook-signature does not exist')

    bot_secrets = secrets.get_secret_value(os.environ['BOT_SECRET_ARN'])

    if secret is not None:
        # New webhook connection
        print('secret is not None')
        
        #Validate there is not an active webhook connected
        if bot_secrets['webhookSecret'] == "":
            bot_secrets['webhookSecret'] = secret
            print("updated")
            secrets.update_secret(os.environ['BOT_SECRET_ARN'], json.dumps(bot_secrets))
            
            # Callback OK with secret
            return {
                "statusCode": 200,
                "headers": {
                    'X-Hook-Secret': secret
                },
                "body": json.dumps({})
            }
        else:
            # Callback 401 error
            print("webhooksecret is already set")

            return {
                "statusCode": 401,
                "body": json.dumps({})
            }
            
    elif signature is not None:
        # New webhook events
        
        # Validate signature
        if secrets.verify_signature(signature, bot_secrets['webhookSecret'], event['body']):

            # Iterate through events
            event_body = json.loads(event['body'])
            asana_events = event_body['events']
            
            for asana_event in asana_events:

                # Retrieve event information
                action = asana_event['action']
                resource = asana_event['resource']
                user_gid = ""

                # Validate if it is a user initiated event
                # if "user" in asana_event and 'gid' in asana_event['user']:
                if asana_event['user'] is not None and asana_event['user']['gid'] is not None:
                    user_gid = asana_event['user']['gid']

                # Act only on new added tasks submitted through the form
                # ... discard user initiated actions
                # ... only act when added to the right section (no sections)
                # ... Customize these criteria to adjust the criteria for creating a new project
                print(asana_event)
                print(action)
                if action == 'added' and resource['gid'] is not None and user_gid != "" and asana_event['parent'] is not None and asana_event['parent']['resource_type'] == 'section' and asana_event['parent']['gid'] == section_gid:
                    # Initiate new project workflow
                    input = json.dumps({
                        "action": "NEW_PROJECT",
                        "taskId": resource['gid'],
                        "apiKey": bot_secrets['apiKey']
                    })
                    client.start_execution(stateMachineArn=bot_state_machine_arn,input=input)
               
                else:
                    print('Event discarded')

            # Callback OK
            return {
                "statusCode": 200,
                "body": json.dumps({})
            }
        else:
            # Callback 401 unauthorized
            return {
                "statusCode": 401,
                "body": json.dumps({})
            }
        
    else:
        # Callback 401 unauthorized
        return {
            "statusCode": 401,
            "body": json.dumps({})
        }
