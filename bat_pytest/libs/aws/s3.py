import boto3

class S3Lib:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def list_buckets(self):
        response = self.s3.list_buckets()
        return response['Buckets']

    def upload_file(self, file_path, bucket_name, file_name):
        self.s3.upload_file(file_path, bucket_name, file_name)

    def download_file(self, bucket_name, file_name, file_path):
        self.s3.download_file(bucket_name, file_name, file_path)

    def delete_file(self, bucket_name, file_name):
        self.s3.delete_object(Bucket=bucket_name, Key=file_name)

