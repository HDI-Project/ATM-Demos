import boto3
import os

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_folder_contents(bucket, prefix, local_dir):
    for obj in bucket.objects.filter(Prefix=prefix):
        if obj.key != prefix:
            _, filename = os.path.split(obj.key)
            bucket.download_file(obj.key, os.path.join(local_dir, filename))


s3 = boto3.resource('s3')
bucket = s3.Bucket('atm-data-store')

gp_dir = 'gp+bandit-search'
grid_dir = 'grid-search'

local_gp_dir= 'gp_csvs'
local_grid_dir= 'grid_csvs'

csv_dir = 'csvs'


# download gp
prefix = '{}/{}/'.format(gp_dir, csv_dir)
ensure_directory(directory=local_gp_dir)
download_folder_contents(bucket=bucket, prefix=prefix, local_dir=local_gp_dir)

# download grid
prefix = '{}/{}/'.format(grid_dir, csv_dir)
ensure_directory(directory=local_grid_dir)
download_folder_contents(bucket=bucket, prefix=prefix, local_dir=local_grid_dir)