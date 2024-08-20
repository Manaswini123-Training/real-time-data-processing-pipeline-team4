import boto3

def lambda_handler(event, context):
    # Initialize CloudWatch client
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-2')
    
    # Lambda function name to monitor
    lambda_function_name = 'my-lambda-function3'  # Replace with the actual Lambda function name

    # Create a CloudWatch Alarm for Lambda invocation errors
    cloudwatch.put_metric_alarm(
        AlarmName='LambdaInvocationErrors',  # Name of the alarm
        MetricName='Errors',  # Metric to monitor
        Namespace='AWS/Lambda',  # Lambda's metric namespace
        Dimensions=[
            {
                'Name': 'FunctionName',  # Dimension to specify Lambda function
                'Value': lambda_function_name
            },
        ],
        Statistic='Sum',  # Aggregation type (Sum of errors)
        Period=300,  # Check period (in seconds), e.g., every 5 minutes
        EvaluationPeriods=1,  # Number of evaluation periods
        Threshold=1,  # Threshold for triggering the alarm
        ComparisonOperator='GreaterThanOrEqualToThreshold',  # Trigger when errors >= 1
        AlarmActions=[
            'arn:aws:sns:us-east-2:471112917983:EcommerceTransactionNotifications'  # SNS topic ARN for notifications
        ],
        TreatMissingData='notBreaching'  # Ignore periods with no data
    )

    print("CloudWatch Alarm for Lambda Invocation Errors created.")
    return {
        'statusCode': 200,
        'body': 'CloudWatch alarm setup successfully.'
    }
