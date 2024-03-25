import boto3

TEXT_BBOX_IMG_PATH = 'rekognition/text_ppt_with_context_01.jpg'


def textract_detect_text(text_bbox_img_path):
    textract = boto3.client('textract', region_name='ap-northeast-2')

    with open(text_bbox_img_path, 'rb') as file:
        img = file.read()

    response = textract.detect_document_text(Document={'Bytes': img})
    text_detections = response['Blocks']

    return text_detections


if __name__ == "__main__":
    file_path = TEXT_BBOX_IMG_PATH

    text_detections = textract_detect_text(file_path)

    for item in text_detections:
        if item['BlockType'] == 'LINE':
            print(item['Text'])
