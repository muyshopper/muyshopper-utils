"""Image utils."""
from muyshopper.utils.slug import create_product_slug
from muyshopper.utils.images import download_upload_image
from muyshopper.utils.space import (
    get_product_images_in_space_online,
    get_product_images_in_space,
    store_images_in_space,
    has_thumbnail,
    create_s3_path,
)


IMAGES_PER_PRODUCT = 4


class ImageManager:
    """Manage images of products in space."""

    def __init__(self):
        """Initialize variables."""
        pass

    def manage_product_images_online(self, item):
        """Manage product images online."""
        # Create product slug
        slug = create_product_slug(item)
        # filter_prefix = os.path.join(S3_IMAGES_PATH, product_slug) + '/'

        # Check if we need to download images for this product
        images_in_space = get_product_images_in_space_online(slug)

        if len(images_in_space) >= 4:
            return

        # Check if store images are already downloaded
        store = item['empresa'].lower()

        for image in images_in_space:
            if store in image:
                return

        # We need to downlad images
        images_to_download_count = IMAGES_PER_PRODUCT - len(images_in_space)

        image_links = item['image_urls'][:images_to_download_count]

        count = 1

        if len(image_links) == 0:
            return

        for image_url in image_links:
            # If image_url is invalid, skip image_url
            if '?' in image_url:
                continue

            # If extension is invalid, skip image_url
            extension = image_url.split('.')[-1]

            if len(extension) > 3:
                continue

            # Create space url
            s3_path = create_s3_path(slug, store, count, extension)

            # Check if we need a thumbnail
            need_thumbnail = True

            if not has_thumbnail(slug) and count <= 1:
                need_thumbnail = True

            # Process image
            data = download_upload_image(
                image_url,
                s3_path,
                thumbnail=need_thumbnail,
            )

            if data['image']:
                images_in_space.append(
                    'https://mmuu-data.nyc3.cdn.digitaloceanspaces.com/' + data['image']
                )

            count += 1

        return images_in_space


    def manage_product_images(self, item):
        """Manage product images."""
        # Create product slug
        slug = create_product_slug(item)
        # filter_prefix = os.path.join(S3_IMAGES_PATH, product_slug) + '/'

        # Check if we need to download images for this product
        images_in_space = get_product_images_in_space(slug)

        if len(images_in_space) >= 4:
            return

        # Check if store images are already downloaded
        store = item['empresa'].lower()

        if store_images_in_space(slug, store):
            return

        # We need to downlad images
        images_to_download_count = IMAGES_PER_PRODUCT - images_in_space

        image_links = item['image_urls'][:images_to_download_count]

        count = 1

        if len(image_links) == 0:
            return

        for image_url in image_links:
            # If image_url is invalid, skip image_url
            if '?' in image_url:
                continue

            # If extension is invalid, skip image_url
            extension = image_url.split('.')[-1]

            if len(extension) > 3:
                continue

            # Create space url
            s3_path = create_s3_path(slug, store, count, extension)

            # Check if we need a thumbnail
            need_thumbnail = False

            if not has_thumbnail_online(slug) and count <= 1:
                need_thumbnail = True

            # Process image
            data = download_upload_image(
                image_url,
                s3_path,
                thumbnail=need_thumbnail,
            )

            if data['image']:
                images_in_space.append(data['image'])

            count += 1
