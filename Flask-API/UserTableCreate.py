import boto3

dynamodb = boto3.resource('dynamodb-local',endpoint_url='http://dynamodb-local:8000', region_name='us-west-2')

table = dynamodb.create_table(
    TableName='Users',
    KeySchema=[
        {'AttributeName': 'PK', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'SK', 'KeyType': 'RANGE'}  # Sort key
    ],
    AttributeDefinitions=[
        {'AttributeName': 'PK', 'AttributeType': 'S'},
        {'AttributeName': 'SK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1SK', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)