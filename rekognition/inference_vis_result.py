# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont

import os
from dotenv import load_dotenv
load_dotenv()
S3_BUCKET = os.getenv('S3_BUCKET')
PROJECT_VERSION_ARN = os.getenv('PROJECT_VERSION_ARN_3')
IMG_PATH = 'assets/cactus_test/test_ppt.jpg'
RESULT_PATH = 'rekognition/result'
MIN_CONFIDENCE = 80


def display_image(bucket, photo, response):
    # Load image from S3 bucket
    s3_connection = boto3.client('s3', region_name='ap-northeast-2')

    s3_object = s3_connection.Object(bucket, photo)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream)

    # Ready image to draw bounding boxes on it.
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    # calculate and display bounding boxes for each detected custom label
    print('Detected custom labels for ' + photo)
    for customLabel in response['CustomLabels']:
        print('Label ' + str(customLabel['Name']))
        print('Confidence ' + str(customLabel['Confidence']))
        if 'Geometry' in customLabel:
            box = customLabel['Geometry']['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']

            fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 50)
            draw.text(
                (left, top), customLabel['Name'], fill='#00d400', font=fnt)

            print('Left: ' + '{0:.0f}'.format(left))
            print('Top: ' + '{0:.0f}'.format(top))
            print('Label Width: ' + "{0:.0f}".format(width))
            print('Label Height: ' + "{0:.0f}".format(height))

            points = (
                (left, top),
                (left + width, top),
                (left + width, top + height),
                (left, top + height),
                (left, top))
            draw.line(points, fill='#00d400', width=5)

    image.show()


def save_bounding_box_images(bucket, photo, labels, output_path):
    # Load image from S3 bucket
    s3_connection = boto3.client('s3', region_name='ap-northeast-2')
    s3_object = s3_connection.get_object(Bucket=bucket, Key=photo)
    stream = io.BytesIO(s3_object['Body'].read())
    image = Image.open(stream)

    # Image dimensions
    imgWidth, imgHeight = image.size

    # Process each detected custom label
    for index, customLabel in enumerate(labels, start=1):
        if 'Geometry' in customLabel:
            box = customLabel['Geometry']['BoundingBox']
            left = int(imgWidth * box['Left'])
            top = int(imgHeight * box['Top'])
            width = int(imgWidth * box['Width'])
            height = int(imgHeight * box['Height'])

            # Define the bounding box area to crop
            area = (left, top, left + width, top + height)
            cropped_image = image.crop(area)

            # Save the cropped image
            file_name = f"{output_path}/label_{index}.jpg"
            cropped_image.save(file_name)
            print(f"Saved {file_name}")


def show_custom_labels(model, bucket, photo, min_confidence):
    client = boto3.client('rekognition', region_name='ap-northeast-2')

    # Call DetectCustomLabels
    response = client.detect_custom_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                           MinConfidence=min_confidence,
                                           ProjectVersionArn=model)

    # For object detection use case, uncomment below code to display image.
    # display_image(bucket,photo,response)

    return response['CustomLabels']


def main():
    bucket = S3_BUCKET
    photo = IMG_PATH
    model = PROJECT_VERSION_ARN
    min_confidence = MIN_CONFIDENCE

    labels = show_custom_labels(model, bucket, photo, min_confidence)

    for label in labels:
        print(f"Label: {label['Name']}")
        print(f"Confidence: {label['Confidence']}")
        if 'Geometry' in label:
            print(f"Geometry: {label['Geometry']}")

    output_path = RESULT_PATH
    save_bounding_box_images(bucket, photo, labels, output_path)


if __name__ == "__main__":
    main()
