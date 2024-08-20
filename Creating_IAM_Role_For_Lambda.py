import boto3
import json
iam = boto3.client('iam')

# Create the role for Lambda
assume_role_policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

role_response = iam.create_role(
    RoleName='LambdaEcommerceProcessingRole',
    AssumeRolePolicyDocument=json.dumps(assume_role_policy_document)
)

role_arn = role_response['Role']['Arn']
print(f"Created IAM Role ARN: {role_arn}")
