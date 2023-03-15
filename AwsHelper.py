import os
import boto3

class AwsHelper:
  def __init__(self, config: dict):
    self.stage = os.environ.get('STAGE') or 'test'
    self.config = config

    self._s3 = None
    self._dynamo_db = None

  @property
  def s3(self):
    if self._s3 is None:
      self._s3 = boto3.resource(self.config['s3'])
    return self._s3
    
  @property
  def dynamo_db(self):
    if self._dynamo_db is None:
      self._dynamo_db = boto3.resource(self.config['dynamo_db'])
    return self._dynamo_db

  @property
  def sqs(self):
    if self._sqs is None:
      self._sqs = boto3.resource(**self.config['sqs'])
    return self._sqs
    
  def get_bucket(self, bucket_name: str):
    return self.s3.Bucket(bucket_name)
    
  def get_table(self, table_name: str):
    return self.dynamo_db.Table(table_name)

  def _get_queue(self, queue_name: str):
    queue = self.sqs.get_queue_by_name(QueueName=queue_name)
    return queue