import pytest
import boto3
from moto import mock_ssm, mock_secretsmanager
import os
from pathlib import Path

print('IN CONFTEST')
moto_credentials_file_path = Path(__file__).parent.absolute() / 'dummy_aws_credentials'


@pytest.fixture(scope='function')
def aws_credentials():
  os.environ['AWS_SHARED_CREDENTIALS_FILE'] = str(moto_credentials_file_path)


@pytest.fixture(scope='function')
def s3(aws_credentials):
  with mock_ssm():
    yield boto3.client('ssm')


@pytest.fixture(scope='function')
def s3(aws_credentials):
  with mock_secretsmanager():
    yield boto3.client('secretsmanager')