# Attach AmazonDynamoDBFullAccess policy
import boto3
import json
iam = boto3.client('iam')
iam.attach_role_policy(
    RoleName='LambdaEcommerceProcessingRole',
    PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess'
)

# Attach AmazonSQSFullAccess policy
iam.attach_role_policy(
    RoleName='LambdaEcommerceProcessingRole',
    PolicyArn='arn:aws:iam::aws:policy/AmazonSQSFullAccess'
)

# Attach AmazonSNSFullAccess policy
iam.attach_role_policy(
    RoleName='LambdaEcommerceProcessingRole',
    PolicyArn='arn:aws:iam::aws:policy/AmazonSNSFullAccess'
)

# Attach AWSLambdaBasicExecutionRole policy (for CloudWatch logs)
iam.attach_role_policy(
    RoleName='LambdaEcommerceProcessingRole',
    PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
)

# Attach AWSLambdaBasicExecutionRole policy (for s3 logs)
iam.attach_role_policy(
    RoleName='LambdaEcommerceProcessingRole',
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
)
