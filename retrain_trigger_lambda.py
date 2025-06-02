import boto3

def lambda_handler(event, context):
    sm = boto3.client('sagemaker')
    
    # Launch SageMaker Pipeline
    response = sm.start_pipeline_execution(
        PipelineName='StrokePredictionPipeline',  # Replace with your pipeline name
    )
    
    print(f"Pipeline execution started: {response['PipelineExecutionArn']}")
    return {'statusCode': 200, 'body': 'Retraining triggered'}
