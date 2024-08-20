import boto3
import zipfile
import os

# Initialize Lambda and SQS clients
lambda_client = boto3.client('lambda')

# Define deployment parameters
FUNCTION_NAME = 'my-lambda-function3'
ROLE_ARN = 'arn:aws:iam::471112917983:role/LambdaEcommerceProcessingRole'  # Replace with your IAM role ARN
SQS_QUEUE_ARN = 'arn:aws:sqs:us-east-2:471112917983:EcommerceTransactionQueue'  # Replace with your SQS ARN

def create_lambda_zip(function_file='lambdafunction18.py', zip_filename='lambda_function18.zip'):
    """Create a ZIP file containing the Lambda function code."""
    if not os.path.exists(function_file):
        raise FileNotFoundError(f"Function file {function_file} not found")
    
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(function_file, os.path.basename(function_file))

def deploy_lambda_function():
    """Deploy or update the Lambda function."""
    try:
        # Create a zip file for the Lambda function
        create_lambda_zip()

        # Read the ZIP file
        with open('lambda_function18.zip', 'rb') as f:
            zip_content = f.read()

        try:
            # Check if the function already exists
            lambda_client.get_function(FunctionName=FUNCTION_NAME)
            # Update function if it exists
            lambda_client.update_function_code(
                FunctionName=FUNCTION_NAME,
                ZipFile=zip_content
            )
            print("Lambda function updated successfully.")
        except lambda_client.exceptions.ResourceNotFoundException:
            # Create the function if it does not exist
            lambda_client.create_function(
                FunctionName=FUNCTION_NAME,
                Runtime='python3.9',  # Adjust runtime if needed
                Role=ROLE_ARN,
                Handler='lambdafunction18.lambda_handler',  # Ensure this matches the handler in your code
                Code={
                    'ZipFile': zip_content
                },
                Environment={
                    'Variables': {
                        'SQS_QUEUE_ARN': SQS_QUEUE_ARN
                    }
                }
            )
            print("Lambda function created successfully.")
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error deploying Lambda function: {e}")

def link_lambda_to_sqs():
    """Create or update the SQS event source mapping for Lambda."""
    try:
        # List existing event source mappings to find the one with the same SQS ARN
        response = lambda_client.list_event_source_mappings(
            EventSourceArn=SQS_QUEUE_ARN,
            FunctionName=FUNCTION_NAME
        )
        
        if response['EventSourceMappings']:
            # Update the existing event source mapping
            for mapping in response['EventSourceMappings']:
                lambda_client.update_event_source_mapping(
                    UUID=mapping['UUID'],
                    Enabled=True,
                    BatchSize=10  # Adjust batch size if needed
                )
            print(f"Successfully updated SQS to Lambda mapping: {response['EventSourceMappings'][0]['UUID']}")
        else:
            # Create a new event source mapping if one doesn't exist
            response = lambda_client.create_event_source_mapping(
                EventSourceArn=SQS_QUEUE_ARN,
                FunctionName=FUNCTION_NAME,
                Enabled=True,
                BatchSize=10  # Adjust batch size if needed
            )
            print(f"Successfully linked SQS to Lambda: {response['UUID']}")
            
    except Exception as e:
        print(f"Error linking SQS to Lambda: {e}")

if __name__ == '__main__':
    deploy_lambda_function()
    link_lambda_to_sqs()
