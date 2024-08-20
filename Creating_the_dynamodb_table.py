import boto3

dynamodb = boto3.client('dynamodb', region_name='us-east-2')

# Create the DynamoDB table
response = dynamodb.create_table(
    TableName='EcommerceTransactions36',
    KeySchema=[
        {
            'AttributeName': 'TransactionID',
            'KeyType': 'HASH'  # Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'TransactionID',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait for the table to be created
dynamodb.get_waiter('table_exists').wait(TableName='EcommerceTransactions36')
print(f"DynamoDB Table 'EcommerceTransactions36' created successfully.")
