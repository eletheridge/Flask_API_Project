import boto3
import os
import base64


class S3:
    """
    Class to handle S3 calls
    """
    def __init__(self, region='us-east-1'):
        self.s3 = boto3.client('s3',
                               endpoint_url='http://localstack:4566',
                               aws_access_key_id='foo',  # localstack does not validate real credentials
                               aws_secret_access_key='bar',  # These would be hidden in a production environment with AWS
                               aws_session_token='foobar')
        self.region = region

    def create_bucket(self, bucket, region=None):
        """
        Creates bucket in S3
        :return: Result of bucket creation
        """
        try:
            if region is None:
                self.s3.create_bucket(Bucket=bucket)
            else:
                self.s3.create_bucket(Bucket=bucket,
                                      CreateBucketConfiguration={{"LocationConstraint": region}})
        except Exception as e:
            return str(e)
        return "Success"

    def upload_file(self, file, bucket, object_name=None):
        """
        Uploads file to S3
        :return: Result of file upload
        """
        if object_name is None:
            object_name = file
        try:
            convert_base64_to_file(file, '/docs/temp_file')
            self.s3.upload_file('/docs/temp_file', bucket, object_name)
        except Exception as e:
            return str(e)
        os.remove("/docs/temp_file")
        return "Success"

    def download_file(self, bucket, object_name, filename='/docs/temp_download_file'):
        """
        Downloads file from S3
        :param bucket: Bucket to download from
        :param object_name: Object to download
        :param filename: File to download to
        :return: Result of file download
        """
        try:
            self.s3.download_file(bucket, object_name, filename)
        except Exception as e:
            return str(e), None
        data = convert_file_to_base64(filename)
        os.remove('/docs/temp_download_file')
        return "Success", data


def convert_base64_to_file(base64_string, filename):
    """
    Converts base64 string to file
    :param base64_string: Base64 string to be converted
    :param filename: Name of file to be created
    :return: True if successful, error if not
    """
    try:
        with open(filename, "wb") as fh:
            fh.write(base64.b64decode(base64_string))
        return True
    except Exception as e:
        return e


def convert_file_to_base64(filename):
    """
    Converts file to base64 string
    :param filename:
    :return: Base64 string
    """
    try:
        with open(filename, "rb") as fh:
            result = base64.b64encode(fh.read())
        return result.decode('utf-8')
    except Exception as e:
        raise Exception(e)
