# Project from Task automation

This project contains source code and supporting files for a demonstration Asana automation.

## Objective

Create an automation using the Asana API that creates a new project from a request

## Architecture

This project is an AWS serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- _bot/_ - Code for the application's main Lambda function. Exposed using an API Gateway
- _newProject/_ - Code for the Lambda function that manages the new project workflow
- _template.yaml_ - A template that defines the application's AWS resources

The application uses several AWS resources, including:

- Lambda functions
- API Gateway API
- Step Functions

These resources are defined in the `template.yaml` file in this project.

The application was developed using [VS Code](https://code.visualstudio.com/) and the [AWS Toolkit](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html), an open source plug-in for popular IDEs that uses the SAM CLI to build and deploy serverless applications on AWS.

## Deploy the application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

- SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Python 3 installed](https://www.python.org/downloads/)
- Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

### Configuration

Before buidling, you will need to update the `constants.py` file in the `newProject/` directory to reference the project you would like use as a template for new projects this app creates. You can get this from the Asana app URL when viewing that project. For example, a project URL might look like: https://app.asana.com/0/\[1234567890\]/board where `1234567890` is the project ID, so you would set PROJECT_TEMPLATE_GID = "1234567890".

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

- **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
- **AWS Region**: The AWS region you want to deploy your app to.
- **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
- **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
- **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

Once deployed, you'll need to input your Asana API key in the newly-created Secrets Manager instance.

You'll also need to initiate your first Webhook that listens to your main project for when a task is moved to the correct section. Follow the documentation here: [Establish a Webhook](https://developers.asana.com/docs/establish-a-webhook).

Use a body like the following to listen to the relevant section of your project. Optionally, you can use any other event filter you'd like to trigger this automation.

```
{
  "data": {
    "filters": [
      {
        "action": "added",
        "resource_type": "task"
      }
    ],
    "resource": "Your Section ID",
    "target": "your API GateWay URL"
  }
}
```

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Use the SAM CLI to build and test locally

### Add local variables

Create a _.env.local_ file and include an environment variable for the Asana API Key, as follows:

```json
{
  "Parameters": {
    "ASANA_API_KEY": ""
  }
}
```

### Build locally

Build your application with the `sam build --use-container` command.

```bash
$ sam build --use-container
```

The SAM CLI installs dependencies defined in each functions' `*/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

### Test the Lambda functions locally

Run functions locally and invoke them with the `sam local invoke` command.

```bash
$ sam local invoke ReviewDatesFunction --event events/changed.json  --env-vars .env.json
```

### Test the API Gateway locally

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
$ sam local start-api
$ curl http://localhost:3000/
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. For our application there is a single function with the `Events` property, referenced as follows:

```yaml
Events:
  Bot:
    Type: Api
    Properties:
      Path: /bot
      Method: post
```

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
$ sam logs -n ReviewDatesFunction --stack-name YOUR_STACK --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Deploying to AWS

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name YOUR_STACK
```

Substitute `YOUR_STACK` for your stack name selected during deployment.

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.
