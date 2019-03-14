"""Parallel download from DigitalOcean Space."""
import logging
import argparse

from multiprocessing import Pool
from muyshopper.utils.space import download_file
from muyshopper.utils.space import get_prefix_keys


DEFAULT_WORKERS = 10


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='DigitalOcean space parallel download manager',
    )

    parser.add_argument(
        '-p', '--prefix',
        required=True,
        help='Filtering prefix'
    )

    parser.add_argument(
        '-w', '--workers',
        required=False,
        help='Number of workers'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    prefix = args.prefix
    workers = int(args.workers) if args.workers else DEFAULT_WORKERS

    file_list = get_prefix_keys(prefix=prefix)

    p = Pool(workers)

    results = p.map(
        download_file,
        [path for path in file_list]
    )

    p.close()
