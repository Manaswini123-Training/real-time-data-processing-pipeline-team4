import boto3

# Create SNS client
sns = boto3.client('sns', region_name='us-east-2')

# Create an SNS topic
response = sns.create_topic(Name='EcommerceTransactionNotifications')
topic_arn = response['TopicArn']
print(f"Created SNS Topic ARN: {topic_arn}")
