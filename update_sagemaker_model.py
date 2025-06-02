import boto3
import time

model_name = f"stroke-pred-model-{int(time.time())}"  # Unique model name with timestamp
endpoint_name = "stroke-pred-endpoint"  # Existing endpoint name
s3_model_uri = "s3://2124323strokepred/ml-project/output/linear-learner-2025-05-27-10-28-33-393/output/model.tar.gz"
image_uri = "811284229777.dkr.ecr.us-east-1.amazonaws.com/linear-learner:1"  # SageMaker Linear Learner image
sagemaker_role_arn = "arn:aws:iam::<your-account-id>:role/<your-sagemaker-execution-role>"  # Replace with your SageMaker execution role

# Initialize SageMaker client
sm_client = boto3.client("sagemaker")

# Step 1: Create a new Model
try:
    print(f"Creating SageMaker Model: {model_name}")
    sm_client.create_model(
        ModelName=model_name,
        ExecutionRoleArn=sagemaker_role_arn,
        PrimaryContainer={
            "Image": image_uri,
            "ModelDataUrl": s3_model_uri
        }
    )
except sm_client.exceptions.ClientError as e:
    print(f"Error creating model: {e}")
    exit(1)

# Step 2: Create a new Endpoint Configuration
endpoint_config_name = f"stroke-pred-endpoint-config-{int(time.time())}"

try:
    print(f"Creating Endpoint Config: {endpoint_config_name}")
    sm_client.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[
            {
                "VariantName": "AllTraffic",
                "ModelName": model_name,
                "InstanceType": "ml.m5.xlarge",  # Update instance type if needed
                "InitialInstanceCount": 1
            }
        ]
    )
except sm_client.exceptions.ClientError as e:
    print(f"Error creating endpoint config: {e}")
    exit(1)

# Step 3: Update the Endpoint
try:
    print(f"Updating Endpoint: {endpoint_name}")
    sm_client.update_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=endpoint_config_name
    )
    print("Update initiated successfully!")
except sm_client.exceptions.ClientError as e:
    print(f"Error updating endpoint: {e}")
    exit(1)
