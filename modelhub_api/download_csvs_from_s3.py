import argparse
import os

import boto3


def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def download_folder_contents(bucket, prefix, local_dir):
    for obj in bucket.objects.filter(Prefix=prefix):
        if obj.key != prefix:
            filename = os.path.join(local_dir, os.path.split(obj.key)[-1])
            print('Downloading S3:{}/{} as {}'.format(bucket.name, obj.key, filename))
            bucket.download_file(obj.key, filename)


def download(bucket, remote_dir, local_dir, csvs_dir):
    prefix = '{}/{}/'.format(remote_dir, csvs_dir)
    ensure_directory(directory=local_dir)
    download_folder_contents(bucket=bucket, prefix=prefix, local_dir=local_dir)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Download ATM datasets.')
    parser.add_argument('-r', '--runtype', type=str, choices=['gp', 'grid'],
                        default=['gp', 'grid'], nargs='*',
                        help='Get only the specified ATM run (gp or grid).')
    parser.add_argument('-b', '--bucket', type=str, default='atm-data-store',
                        help='S3 Bucket name (defaults to atm-data-store).')
    parser.add_argument('--gp-dir', type=str, default='gp+bandit-search')
    parser.add_argument('--grid-dir', type=str, default='grid-search')
    parser.add_argument('--local-gp-dir', type=str, default='gp_csvs')
    parser.add_argument('--local-grid-dir', type=str, default='grid_csvs')
    parser.add_argument('--csvs-dir', type=str, default='csvs')

    args = parser.parse_args()

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(args.bucket)

    if 'gp' in args.runtype:
        download(bucket, args.gp_dir, args.local_gp_dir, args.csvs_dir)

    if 'grid' in args.runtype:
        download(bucket, args.grid_dir, args.local_grid_dir, args.csvs_dir)
