import boto3

import os
from dotenv import load_dotenv
load_dotenv()
PROJECT_VERSION_ARN = os.getenv('PROJECT_VERSION_ARN_3')


def detect_custom_labels(image_path):
    client = boto3.client('rekognition', region_name='ap-northeast-2')

    with open(image_path, 'rb') as image:
        response = client.detect_custom_labels(
            ProjectVersionArn=PROJECT_VERSION_ARN,
            Image={'Bytes': image.read()},
        )

    for label in response['CustomLabels']:
        print(f"Label: {label['Name']}")
        print(f"Confidence: {label['Confidence']}")
        if 'Geometry' in label:
            print(f"Geometry: {label['Geometry']}")


image_path = 'rekognition/text_ppt_with_context_01.jpg'
detect_custom_labels(image_path)
