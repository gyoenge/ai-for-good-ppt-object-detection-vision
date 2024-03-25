import boto3

TEXT_BBOX_IMG_PATH = 'rekognition/text_ppt_with_context_01.jpg'


def rekognition_detect_text(text_bbox_img_path):
    rekognition = boto3.client('rekognition', region_name='ap-northeast-2')

    with open(text_bbox_img_path, 'rb') as image:
        response = rekognition.detect_text(Image={'Bytes': image.read()})

    text_detections = response['TextDetections']

    line_texts = {det['Id']: det['DetectedText']
                  for det in text_detections if det['Type'] == 'LINE'}
    word_texts = {}
    for det in text_detections:
        if det['Type'] == 'WORD':
            if det['ParentId'] in word_texts:
                word_texts[det['ParentId']] += ' ' + det['DetectedText']
            else:
                word_texts[det['ParentId']] = det['DetectedText']

    return line_texts, word_texts


def extract_text_by_line(text_bbox_img_path):
    line_texts, word_texts = rekognition_detect_text(text_bbox_img_path)
    combined_texts_by_line = [
        line_texts[line_id] if line_id not in word_texts else word_texts[line_id] for line_id in line_texts]

    return combined_texts_by_line


def extract_text_by_allcombined(text_bbox_img_path):
    line_texts, word_texts = rekognition_detect_text(text_bbox_img_path)
    combined_texts_by_line = extract_text_by_line(line_texts, word_texts)
    combined_texts_all = ' '.join(combined_texts_by_line)

    return combined_texts_all


if __name__ == "__main__":
    file_path = TEXT_BBOX_IMG_PATH

    # combined_texts_by_line = extract_text_by_line(file_path)
    # for text_line in combined_texts:
    #     print(text_line)

    combined_texts_all = extract_text_by_allcombined(file_path)
    print(combined_texts_all)
