import boto3
from botocore import UNSIGNED
from botocore.config import Config


def contact_s3():
    # Create a client for the S3 service
    s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))

    # Specify the bucket name
    bucket_name = "some_bucket_with_daily_data"

    # List objects in the bucket
    response = s3_client.list_objects(Bucket=bucket_name)

    # list the contents of the response
    events = []
    for object in response["Contents"]:
        events.append(object["Key"])

    # Ignore metadata pdf
    events = [i for i in events if i != "about_data.pdf"]

    print(f"Number of events in bucket: {len(events)}. \n Head: {events[:2]} (...)")

    return s3_client, bucket_name, events
