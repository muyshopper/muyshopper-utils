"""Redis DB manager utils."""
import os
import json
import redis


DEFAULT_KEY = os.environ['REDIS_KEY']


def get_redis_client():
    """Create a redis client object."""
    redis_host = os.environ['REDIS_HOST']
    redis_port = os.environ['REDIS_PORT']
    redis_password = os.environ['REDIS_PASSWORD']

    client = redis.Redis(
        host=redis_host, 
        port=redis_port,
        password=redis_password,
    )

    return client


def save_item_to_redis(item, key=DEFAULT_KEY):
    """Save item to redis database."""
    client = get_redis_client()
    client.rpush(key, item)


def get_item_from_redis(key=DEFAULT_KEY, is_dict=True):
    """Get item from redis database."""
    client = get_redis_client()

    item = client.lpop(key)

    if type(item) == bytes:
        item = item.decode('utf-8')

    if item and is_dict:
        try:
            return json.loads(item[1])
        except:
            return json.loads(item)
    
    return item 


def get_item_count(key=DEFAULT_KEY):
    """Get item count in a redis database key."""
    client = get_redis_client()
    
    return client.llen(DEFAULT_KEY)


def clear_key_items(key=DEFAULT_KEY):
    """Remove all items in key."""
    client = get_redis_client()

    client.delete(key)
