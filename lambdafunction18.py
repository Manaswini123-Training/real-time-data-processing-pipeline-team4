import json
import boto3
import os
from decimal import Decimal

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

# Initialize SNS client
sns_client = boto3.client('sns', region_name='us-east-2')

# Retrieve DynamoDB table name from environment variables
table_name = os.getenv('DYNAMODB_TABLE_NAME', 'EcommerceTransactions36')

# Initialize DynamoDB Table
table = dynamodb.Table(table_name)

# SNS topic ARN
sns_topic_arn = os.getenv('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-2:471112917983:EcommerceTransactionNotifications')

def lambda_handler(event, context):
    """Main Lambda handler function that processes SQS messages and stores them in DynamoDB."""
    
    # Process each record in the SQS event
    for record in event['Records']:
        try:
            # The SQS message body contains the data (which is in JSON format)
            message_body = json.loads(record['body'])
            
            print(f"Processing message from SQS: {message_body}")
            
            # Process the data if needed (transform the message)
            processed_data = process_data(message_body)
            
            # Validate the processed data
            if validate_data(processed_data):
                # Store the processed data in DynamoDB
                store_in_dynamodb(processed_data)
                
                # Check conditions and send email notifications
                check_conditions_and_notify(processed_data)
            else:
                print(f"Validation failed for data: {processed_data}")
        except Exception as e:
            print(f"Error processing record: {e}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Messages processed successfully')
    }

def process_data(data):
    """Process and transform the data if needed."""
    # Convert float to Decimal to avoid DynamoDB issues
    if isinstance(data.get('Price'), float):
        data['Price'] = Decimal(str(data['Price']))
    if isinstance(data.get('TotalAmount'), float):
        data['TotalAmount'] = Decimal(str(data['TotalAmount']))
    
    return data

def validate_data(data):
    """Validate the incoming data."""
    if not data.get('TransactionID'):
        print("Validation Error: Missing TransactionID")
        return False
    if not data.get('CustomerID'):
        print("Validation Error: Missing CustomerID")
        return False
    if not data.get('ItemName'):
        print("Validation Error: Missing ItemName")
        return False
    if not isinstance(data.get('Quantity'), int) or data['Quantity'] <= 0:
        print("Validation Error: Quantity should be a positive integer")
        return False
    if not isinstance(data.get('Price'), (Decimal, int)) or data['Price'] <= 0:
        print("Validation Error: Price should be a positive number")
        return False
    return True

def store_in_dynamodb(data):
    """Store the processed data in DynamoDB."""
    try:
        table.put_item(
            Item={
                'TransactionID': data['TransactionID'],  # Primary key
                'CustomerID': data['CustomerID'],
                'ItemName': data['ItemName'],
                'Quantity': data['Quantity'],  # Assuming Quantity is an integer
                'Price': data['Price'],  # Decimal type
                'TotalAmount': data['TotalAmount'],  # Decimal type
                'PaymentMethod': data['PaymentMethod'],
                'OrderStatus': data['OrderStatus']
            }
        )
        print("Data successfully stored in DynamoDB.")
    except Exception as e:
        print(f"Error storing data in DynamoDB: {e}")
        raise e

def check_conditions_and_notify(data):
    """Check specific conditions and send email notifications via SNS."""
    # Condition 1: Payment method is PayPal
    if data['PaymentMethod'] == 'PayPal':
        message = f"Payment through PayPal detected for TransactionID: {data['TransactionID']}"
        send_email_notification(message, data['CustomerEmail'])
    
    # Condition 2: Order status is pending
    if data['OrderStatus'].lower() == 'pending':
        message = f"Order status is pending for TransactionID: {data['TransactionID']}"
        send_email_notification(message, data['CustomerEmail'])

def send_email_notification(message, recipient_email):
    """Send an email notification using SNS."""
    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject='Ecommerce Transaction Alert',
            MessageAttributes={
                'recipient': {
                    'DataType': 'String',
                    'StringValue': recipient_email
                }
            }
        )
        print(f"Notification sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending notification: {e}")
        raise e
