"""MuyShopper images utils."""
import os
import uuid
import shutil
import requests

from PIL import Image

from muyshopper.utils.space import upload_file_to_s3


# Image Settings
BIG_W_H = (500, 500)
THUMB_W_H = (200, 200)

# Temp folder
TMP_FOLDER = '/tmp'


class LowImageQualityException(Exception):
    """Raise when image quality is low."""

    pass


def download_valid_image_from_url(url, path):
    """Download image while making sure it's big enough."""
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

        img = Image.open(path)
        w, h = img.size

        name, ext = os.path.splitext(path)
        optimized_name = name + '-optimized.jpg'

        optimize_and_save_image(img, img.size, optimized_name)

        if w < 200 or h < 200:
            raise LowImageQualityException

        return optimized_name
    else:
        raise Exception


def optimize_and_save_image(img, size, output_path, quality=80):
    """Optimize image and save it."""
    img.thumbnail(
        size,
        resample=Image.ANTIALIAS,
    )

    save_args = {
        'format': 'jpeg',
        'quality': quality,
        'progressive': True,
    }

    img.save(output_path, **save_args)


def make_thumbnail(local_path, s3_path):
    """Create a thumbnail for a certain image."""
    img = Image.open(local_path)

    name, ext = os.path.splitext(local_path)
    optimized_name = name + '-optimized-thumb.jpg'

    optimize_and_save_image(img, THUMB_W_H, optimized_name)

    thumbnail_s3_path = s3_path.replace('big', 'thumb')

    img.save(optimized_name)

    return optimized_name, thumbnail_s3_path


def download_upload_image(image_url, s3_path, thumbnail=False):
    """Download image and upload it to the space."""
    filename, ext = os.path.splitext(image_url)
    tmp_path = os.path.join(TMP_FOLDER, str(uuid.uuid4()) + ext)

    data = {}

    try:
        optimized_path = download_valid_image_from_url(
            image_url,
            tmp_path,
        )

        upload_file_to_s3(optimized_path, s3_path)

        data['image'] = s3_path

        if thumbnail:
            thumb_path, thumb_s3_path = make_thumbnail(
                optimized_path,
                s3_path,
            )

            upload_file_to_s3(thumb_path, thumb_s3_path)

            data['thumbnail'] = thumb_s3_path

        return data
    except LowImageQualityException:
        return
