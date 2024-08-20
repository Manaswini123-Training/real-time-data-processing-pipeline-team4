import boto3

# Initialize the SNS client
sns_client = boto3.client('sns', region_name='us-east-2')

# Details for the subscription
topic_arn = 'arn:aws:sns:us-east-2:471112917983:EcommerceTransactionNotifications'
protocol = 'email'
endpoint = 'sulgutisaikoushikreddy@gmail.com'

try:
    # Create the subscription
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol=protocol,
        Endpoint=endpoint,
        ReturnSubscriptionArn=True
    )

    subscription_arn = response['SubscriptionArn']
    print(f"Subscription created with ARN: {subscription_arn}")

except Exception as e:
    print(f"Error creating subscription: {e}")
    raise e
