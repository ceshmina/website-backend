from PIL import Image


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


if __name__ == '__main__':
    make_thumbnail('sample.jpg', 'sample_thumbnail.jpg', 256)
