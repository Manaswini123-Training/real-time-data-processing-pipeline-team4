from faker import Faker
import uuid
import random
import json
import boto3

# Initialize Faker and SQS client
fake = Faker()
sqs_client = boto3.client('sqs')

# SQS Queue URL
sqs_queue_url = 'https://sqs.us-east-2.amazonaws.com/471112917983/EcommerceTransactionQueue'

# Generate a single transaction record
def generate_transaction():
    transaction = {
        "TransactionID": str(uuid.uuid4()),
        "CustomerID": fake.uuid4(),
        "ItemID": fake.uuid4(),
        "ItemName": fake.word(),
        "Quantity": random.randint(1, 5),
        "Price": round(random.uniform(10.0, 500.0), 2),
        "TotalAmount": None,
        "PaymentMethod": random.choice(["Credit Card", "PayPal", "Debit Card"]),
        "ShippingAddress": fake.address(),
        "OrderStatus": random.choice(["Pending", "Shipped", "Delivered"]),
        "CustomerEmail": fake.email()
    }
    transaction["TotalAmount"] = round(transaction["Quantity"] * transaction["Price"], 2)
    return transaction

# Generate and send transactions to SQS
def send_transactions_to_sqs(num_transactions):
    for _ in range(num_transactions):
        transaction = generate_transaction()
        try:
            sqs_response = sqs_client.send_message(
                QueueUrl=sqs_queue_url,
                MessageBody=json.dumps(transaction)
            )
            print(f"Message sent to SQS: {sqs_response['MessageId']}")
        except Exception as e:
            print(f"Error sending message to SQS: {e}")

# Specify the number of transactions to send
send_transactions_to_sqs(10)
