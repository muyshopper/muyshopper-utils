"""Slug utils."""

def create_product_slug(item):
    """Create product slug based on item's brand & model fields."""
    item_slug = item['marca'].replace(' ', '-').lower() + '-' \
        + item['modelo'].replace(' ', '-').lower()

    return item_slug
