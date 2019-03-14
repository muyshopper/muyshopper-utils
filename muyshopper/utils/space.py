"""Space utils."""
import os
import boto3


# S3 settings
S3_REGION_NAME = 'nyc3'
S3_SPACE_NAME = 'mmuu-data'
S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
S3_ACCESS_ID = os.getenv('S3_ACCESS_ID')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_IMAGES_PATH = 'img/big/'
S3_THUMBNAILS_PATH = 'img/thumb/'


# Local paths
IMAGES_LIST_PATH = '/tmp/images.txt'
THUMBNAILS_LIST_PATH = '/tmp/thumbnails.txt'


def get_images_list(prefix=S3_IMAGES_PATH):
    """Get a list of images of products present in the Space."""
    session = boto3.session.Session()

    client = session.client(
        's3',
        region_name=S3_REGION_NAME,
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=S3_ACCESS_ID,
        aws_secret_access_key=S3_SECRET_KEY
    )

    image_links = []

    # Create a reusable Paginator
    paginator = client.get_paginator('list_objects')

    # Create a PageIterator from the Paginator
    page_iterator = paginator.paginate(Bucket=S3_SPACE_NAME, Prefix=prefix)

    for page in page_iterator:
        for obj in page['Contents']:
            image_links.append(
                'https://mmuu-data.nyc3.digitaloceanspaces.com/' +
                obj['Key']
            )

    return image_links


def get_prefix_keys(prefix=S3_IMAGES_PATH):
    """Get a list of keys present in the Space with prefix."""
    session = boto3.session.Session()

    client = session.client(
        's3',
        region_name=S3_REGION_NAME,
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=S3_ACCESS_ID,
        aws_secret_access_key=S3_SECRET_KEY
    )

    image_links = []

    # Create a reusable Paginator
    paginator = client.get_paginator('list_objects')

    # Create a PageIterator from the Paginator
    page_iterator = paginator.paginate(Bucket=S3_SPACE_NAME, Prefix=prefix)

    for page in page_iterator:
        for obj in page['Contents']:
            image_links.append(obj['Key'])

    return image_links


def get_thumbnails_list():
    """Get a list of thumbnails of products present in the Space."""
    thumbnail_links = get_images_list(prefix=S3_THUMBNAILS_PATH)

    return thumbnail_links


def download_images_list(filename=IMAGES_LIST_PATH):
    """Download a list of images of products present in the Space."""
    image_links = get_images_list()

    with open(filename, 'w') as fp:
        fp.write('\n'.join(image_links))


def download_thumbnails_list(filename=THUMBNAILS_LIST_PATH):
    """Download a list of thumbnails of products present in the Space."""
    image_links = get_images_list()

    with open(filename, 'w') as fp:
        fp.write('\n'.join(image_links))


def upload_file_to_s3(local_path, s3_path, metadata=None):
    """Upload file to the DigitalOcean space."""
    session = boto3.session.Session()

    client = session.client(
        's3',
        region_name=S3_REGION_NAME,
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=S3_ACCESS_ID,
        aws_secret_access_key=S3_SECRET_KEY
    )

    if metadata:
        extra_args = {
            'ACL': 'public-read',
            'Metadata': metadata
        }
    else:
        extra_args = {
            'ACL': 'public-read',
        }

    client.upload_file(
        local_path,
        S3_SPACE_NAME,
        s3_path,
        ExtraArgs=extra_args
    )

    return os.path.join(S3_ENDPOINT_URL, s3_path)


def read_images_list(filename=IMAGES_LIST_PATH):
    """Read image list from local file."""
    if not os.path.isfile(filename):
        download_images_list()

    with open(filename, 'r') as fp:
        images_list = fp.read().splitlines()

    return images_list


def read_thumbnails_list(filename=THUMBNAILS_LIST_PATH):
    """Read thumbnail list from local file."""
    if not os.path.isfile(filename):
        download_thumbnails_list()

    return read_images_list(filename=filename)


def get_product_images_in_space(slug):
    """Retrieve product data of images and thumbnails on space."""
    product_space_data = {
        'images': [],
        'thumbnails': [],
    }

    images_list = read_images_list()

    product_images_list = [
        img for img in images_list if slug + '/' in img
    ]

    product_space_data['images'].extend(product_images_list)

    thumbnails_list = read_thumbnails_list()

    product_thumbnail_list = [
            img for img in thumbnails_list if slug + '/' in img
    ]

    product_space_data['thumbnails'].extend(product_thumbnail_list)

    return product_space_data


def get_product_images_in_space_online(slug):
    """Get product images in space online."""
    session = boto3.session.Session()

    client = session.client(
        's3',
        region_name=S3_REGION_NAME,
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=S3_ACCESS_ID,
        aws_secret_access_key=S3_SECRET_KEY
    )

    keys = []

    prefix = os.path.join(S3_IMAGES_PATH, slug) + '/'

    response = client.list_objects_v2(Bucket='mmuu-data', Prefix=prefix)

    for item in response.get('Contents', []):
        keys.append(
            'https://mmuu-data.nyc3.digitaloceanspaces.com/' + item['Key']
        )

    return keys[1:]


def get_product_images_in_space_count(slug):
    """Retrieve count of product images in the space."""
    return len(get_product_images_in_space(slug)['images'])


def store_images_in_space(slug, store):
    """Check if store images of a product are already in the space."""
    product_images = get_product_images_in_space(slug)['images']

    store = store.lower()

    for image in product_images:
        if store in image:
            return True

    return False


def has_thumbnail(slug):
    """Check if product has a thumbnail image."""
    return len(get_product_images_in_space(slug)['thumbnails']) > 1


def has_thumbnail_online(slug):
    """Check if product has a thumbnail image online."""
    session = boto3.session.Session()

    client = session.client(
        's3',
        region_name=S3_REGION_NAME,
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=S3_ACCESS_ID,
        aws_secret_access_key=S3_SECRET_KEY
    )

    keys = []

    prefix = os.path.join(S3_THUMBNAILS_PATH, slug) + '/'

    response = client.list_objects_v2(Bucket='mmuu-data', Prefix=prefix)

    for item in response.get('Contents', []):
        keys.append(
            'https://mmuu-data.nyc3.digitaloceanspaces.com/' + item['Key']
        )

    return keys[1:]


def create_s3_path(slug, store, count, extension):
    """Create S3 path."""
    return os.path.join(
        S3_IMAGES_PATH, slug
    ) + '/' + store + '-' + str(count) + '.' + extension


def delete_s3_prefix(prefix):
    """Recursively delete S3 key with prefix."""
    session = boto3.session.Session()

    client = session.client(
        's3',
        region_name=S3_REGION_NAME,
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=S3_ACCESS_ID,
        aws_secret_access_key=S3_SECRET_KEY
    )

    files_to_delete = get_prefix_keys(prefix=prefix)

    for key in files_to_delete:
        print('delete {}'.format(key))
        client.delete_object(Bucket=S3_SPACE_NAME, Key=key)


def download_file(key):
    BASE_PATH = './downloads/'

    basename = os.path.basename(key)

    folder = os.path.join(
        BASE_PATH,
        os.path.dirname(key)
    )

    os.makedirs(folder, exist_ok=True)

    filename = os.path.join(folder, basename)

    if os.path.exists(filename):
        print('Skipping.. {}'.format(key))
        return

    session = boto3.session.Session()

    client = session.client(
        's3',
        region_name=S3_REGION_NAME,
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=S3_ACCESS_ID,
        aws_secret_access_key=S3_SECRET_KEY
    )

    print('Downloading.. {}'.format(key))

    client.download_file(
        Bucket=S3_SPACE_NAME,
        Filename=filename,
        Key=key,
    )