import boto3
import os


def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def download_folder_contents(bucket, prefix, local_dir):
    for obj in bucket.objects.filter(Prefix=prefix):
        _, filename = os.path.split(obj.key)

        bucket.download_file(obj.key, os.path.join(local_dir, filename))


s3 = boto3.resource('s3')
bucket = s3.Bucket('atm-data-store')

main_dir = 'compare-atm-openml-data'
openml_dir = 'openml-results'
gp_dir = 'atm-results-gpbandit-binary'
grid_dir = 'atm-results-grid-binary'
did_name_file = 'openml-did-name-list.csv'


# download openml
prefix = '{}/{}/'.format(main_dir, openml_dir)
ensure_directory(directory=openml_dir)
download_folder_contents(bucket=bucket, prefix=prefix, local_dir=openml_dir)

# download gp
prefix = '{}/{}/'.format(main_dir, gp_dir)
ensure_directory(directory=gp_dir)
download_folder_contents(bucket=bucket, prefix=prefix, local_dir=gp_dir)

# download grid
prefix = '{}/{}/'.format(main_dir, grid_dir)
ensure_directory(directory=grid_dir)
download_folder_contents(bucket=bucket, prefix=prefix, local_dir=grid_dir)

# dowload did-name-file
file_key = '{}/{}'.format(main_dir, did_name_file)
bucket.download_file(file_key, did_name_file)