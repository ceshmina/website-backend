import json

import boto3
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.TiffImagePlugin import IFDRational


s3_client = boto3.client('s3')


def make_thumbnail(image_path: str, thumbnail_path: str, size: int):
    image = Image.open(image_path)
    width, height = image.size
    if width > height:
        new_width = size
        new_height = size * height // width
    else:
        new_height = size
        new_width = size * width // height
    image.thumbnail(size=(new_width, new_height))
    image.save(thumbnail_path)


def _format_value(value):
    if isinstance(value, bytes):
        return value.decode('utf-8')
    elif isinstance(value, IFDRational):
        return float(value.numerator) / float(value.denominator)
    elif isinstance(value, tuple):
        return [_format_value(v) for v in value]
    else:
        return value


def extract_exif(image_path: str, exif_path: str):
    image = Image.open(image_path)
    exif = image._getexif()
    exif_json = { TAGS.get(tag, tag): _format_value(value) for tag, value in exif.items() }
    with open(exif_path, 'w') as f:
        json.dump(exif_json, f, indent=2)


def pipeline(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    if 'medium' not in key or not key.endswith('.jpg'):
        return
    key = key[:-4]

    original_path = f'/tmp/{key}.jpg'
    thumbnail_path = f'/tmp/{key}_thumbnail.jpg'
    exif_path = f'/tmp/{key}_exif.json'
    s3_client.download_file(bucket, f'{key}.jpg', original_path)

    make_thumbnail(original_path, thumbnail_path, 256)
    extract_exif(original_path, exif_path)

    thumbnail_key = key.replace('medium', 'thumbnail')
    exif_key = key.replace('medium', 'exif')
    s3_client.upload_file(thumbnail_path, bucket, f'{thumbnail_key}.jpg')
    s3_client.upload_file(exif_path, bucket, f'{exif_key}.json')


def lambda_handler(event, context):
    try:
        pipeline(event)
    except Exception as e:
        print(e)
        raise e
