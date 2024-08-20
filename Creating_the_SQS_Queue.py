import boto3

# Initialize SQS client
sqs = boto3.client('sqs')

# Create a new SQS queue
def create_sqs_queue(queue_name):
    response = sqs.create_queue(QueueName=queue_name)
    return response['QueueUrl']


queue_name = 'EcommerceTransactionQueue'
queue_url = create_sqs_queue(queue_name)
print(f"Queue created with URL: {queue_url}")
