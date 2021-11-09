# General
import os
import boto3

# Services
from resources.services.file_service import read_file


def upload_file(file_name, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(
            f"{os.getcwd()}/cropped_images/{file_name}", 'bevvy-ocr', object_name)
        print(f'{file_name} uploaded to AWS S3, bucket - bevvy-ocr')
        return True
    except:
        print(f'{file_name} failed to upload to AWS S3, bucket - bevvy-ocr')
        return False


def get_bucket_files():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('bevvy-ocr')
    return bucket.objects.all()


def detect_text(filename, upload):
    credentials = read_file('credentials.json')

    access_key = credentials['amazon']['access_key']
    access_secret = credentials['amazon']['access_secret']

    client = boto3.client(
        'rekognition', aws_access_key_id=access_key, aws_secret_access_key=access_secret)

    if upload == True:
        upload_file(filename)

    response = client.detect_text(
        Image={'S3Object': {'Bucket': 'bevvy-ocr', 'Name': filename}})

    detections = response['TextDetections']

    text = []
    for word in detections:
        text.append(word['DetectedText'])

    text_array = list(dict.fromkeys(text))
    return " ".join(text_array).lower()
