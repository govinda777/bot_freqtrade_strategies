from behave import given, when, then
import boto3

# Configura o cliente S3 apontando para o LocalStack
s3_client = boto3.client('s3', endpoint_url='http://localhost:4566')
dynamodb_client = boto3.client('dynamodb', endpoint_url='http://localhost:4566')

@given('que o bucket "{bucket_name}" não existe')
def step_given_bucket_nao_existe(context, bucket_name):
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    if bucket_name in buckets:
        s3_client.delete_bucket(Bucket=bucket_name)

@when('eu crio o bucket "{bucket_name}"')
def step_when_crio_bucket(context, bucket_name):
    s3_client.create_bucket(Bucket=bucket_name)

@then('o bucket "{bucket_name}" deve existir')
def step_then_bucket_deve_existir(context, bucket_name):
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    assert bucket_name in buckets, f"Bucket {bucket_name} não foi encontrado."

@given('que a tabela "{table_name}" não existe')
def step_given_tabela_nao_existe(context, table_name):
    existing_tables = dynamodb_client.list_tables()['TableNames']
    if table_name in existing_tables:
        dynamodb_client.delete_table(TableName=table_name)

@when('eu crio a tabela "{table_name}" com chave primária "{key}"')
def step_when_crio_tabela(context, table_name, key):
    dynamodb_client.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': key, 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': key, 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

@then('a tabela "{table_name}" deve existir com a chave primária "{key}"')
def step_then_tabela_deve_existir(context, table_name, key):
    existing_tables = dynamodb_client.list_tables()['TableNames']
    assert table_name in existing_tables, f"Tabela {table_name} não foi encontrada."
    table_info = dynamodb_client.describe_table(TableName=table_name)
    key_schema = table_info['Table']['KeySchema']
    assert any(k['AttributeName'] == key for k in key_schema), f"Chave primária {key} não encontrada na tabela."
