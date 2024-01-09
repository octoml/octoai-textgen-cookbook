import boto3

# Initialize clients
apigateway = boto3.client("apigateway")
lambda_client = boto3.client("lambda")

LAMBDA_ARN = "MyLambdaARN"
API_NAME = "MyAPI"
STAGE_NAME = "prod"
RESOURCE_PATH = "askllama"
HTTP_METHOD = "POST"

# Create REST API
response = apigateway.create_rest_api(
    name=API_NAME,
    description="API for " + LAMBDA_ARN,
    endpointConfiguration={"types": ["REGIONAL"]},
)
api_id = response["id"]

# Get the root ID for the API Gateway
response = apigateway.get_resources(restApiId=api_id)
root_id = response["items"][0]["id"]

# Create a resource under root
response = apigateway.create_resource(
    restApiId=api_id, parentId=root_id, pathPart=RESOURCE_PATH
)
resource_id = response["id"]

# Grant API Gateway permissions to invoke the Lambda function
lambda_client.add_permission(
    FunctionName=LAMBDA_ARN,
    StatementId="apigateway-invoke",
    Action="lambda:InvokeFunction",
    Principal="apigateway.amazonaws.com",
)

# Create a POST method for the resource
apigateway.put_method(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod=HTTP_METHOD,
    authorizationType="NONE",
)

# Set the POST method to trigger the Lambda function
apigateway.put_integration(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod=HTTP_METHOD,
    type="AWS_PROXY",
    integrationHttpMethod="POST",
    uri=f"arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{LAMBDA_ARN}/invocations",
)

# Deploy the API to a new stage
apigateway.create_deployment(
    restApiId=api_id, stageName=STAGE_NAME, description="Deploying to " + STAGE_NAME
)

# Create an API key
api_key_response = apigateway.create_api_key(
    name="ClientAPIKey", description="API key for clients", enabled=True
)
api_key = api_key_response["value"]

# Create a usage plan
usage_plan_response = apigateway.create_usage_plan(
    name="ClientUsagePlan",
    description="Usage plan for clients",
    apiStages=[{"apiId": api_id, "stage": STAGE_NAME}],
)

# Associate API key with usage plan
apigateway.create_usage_plan_key(
    usagePlanId=usage_plan_response["id"],
    keyId=api_key_response["id"],
    keyType="API_KEY",
)

print(
    f"API Gateway URL: https://{api_id}.execute-api.us-east-1.amazonaws.com/{STAGE_NAME}/{RESOURCE_PATH}"
)
print(f"API Key for client authentication: {api_key}")
