import json

from PIL import Image
from PIL.ExifTags import TAGS
from PIL.TiffImagePlugin import IFDRational


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


if __name__ == '__main__':
    make_thumbnail('sample.jpg', 'sample_thumbnail.jpg', 256)
    extract_exif('sample.jpg', 'sample_exif.json')
