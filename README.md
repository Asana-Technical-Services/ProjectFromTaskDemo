# Stitch Fix: Asana Automation

This project contains source code and supporting files for the Asana automation created for Stitch Fix.

## Objective

Create an automation using the Asana API that manages the creative request intake process creation.

The [documentation for this project can be found here](https://docs.google.com/document/d/1g5w-l5u0MS_K2TlnSLdE7PVOIbo5aX7Sc76DFYyDjBw/edit?usp=sharing).

## Architecture

This project is an AWS serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- _bot/_ - Code for the application's main Lambda function. Exposed using an API Gateway
- _events/_ - Invocation events that you can use to invoke the functions
- _newProject/_ - Code for the Lambda function that manages the new project workflow
- _reviewDates/_ - Code for the Lambda function that manages the dates review workflow
- _samconfig.toml_ - configuration for deployment and local testing
- _tests/_ - Unit tests for the application code
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

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

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
        StitchFixBot:
          Type: Api 
          Properties:
            Path: /bot
            Method: post
```

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
$ sam logs -n ReviewDatesFunction --stack-name stitch-fix --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name stitch-fix
```

Substitute `stitch-fix` for your stack name selected during deployment.

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.
	