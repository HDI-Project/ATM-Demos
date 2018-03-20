import io
import os
import shutil
import zlib

import boto3
import pandas as pd
from sklearn.externals.joblib.numpy_pickle import NumpyUnpickler

import queries


class ModelhubExplorer(object):

    @staticmethod
    def get_row(df, column, value):
        rows = df[df[column] == value]
        if len(rows) > 1:
            raise Exception("More than one row found!")
        elif len(rows) == 1:
            return rows.iloc[0]

    def read_csv(self, path, *args, **kwargs):
        print('Downloading file {} from S3 bucket'.format(path))
        body = self.bucket.Object(path).get()['Body'].read()
        with io.BytesIO(body) as buf:
            return pd.read_csv(buf, *args, **kwargs)

    def __init__(self, modelhub_bucket_name, modelhub_path):
        self.modelhub_path = modelhub_path
        self.bucket = boto3.resource('s3').Bucket(modelhub_bucket_name)

        self.datasets = self.read_csv(os.path.join(modelhub_path, 'csvs/datasets.csv'))
        self.dataruns = self.read_csv(os.path.join(modelhub_path, 'csvs/dataruns.csv'))
        self.classifiers = self.read_csv(os.path.join(modelhub_path, 'csvs/classifiers.csv'))

    def unique_datasets(self):
        return list(self.datasets.name.unique())

    def download_model(self, model_location):
        key = os.path.join(self.modelhub_path, model_location)
        body = self.bucket.Object(key).get()['Body'].read()
        decomp = zlib.decompress(body)
        return NumpyUnpickler('', io.BytesIO(decomp)).load()

    def get_best_classifier(self, dataset_name, download=True):
        dataset = self.get_row(self.datasets, 'name', dataset_name)
        if dataset is None:
            raise Exception("Invalid dataset name")

        datarun = self.get_row(self.dataruns, 'dataset_id', dataset.dataset_id)
        ds_classifiers = self.classifiers[self.classifiers.datarun_id == datarun.datarun_id]
        row = ds_classifiers.sort_values('test_judgment_metric', ascending=False).iloc[0]

        classifier = queries.Classifier(row)

        if download:
            classifier.model = self.download_model(row.model_location)

        return classifier


# The functions below are work in progress

def download_d3m_dataset(d3m_dataset):
    archive = d3m_dataset + '.tar.gz'
    key = d3m_path + archive
    d3m_bucket.download_file(Key=key, Filename=archive)

    with tarfile.open(archive) as tar:
        tar.extractall()

    # Cleanup
    os.remove(archive)


def get_d3m_data(dataset_name):
    d3m_dataset = get_row(overlap, 'name', dataset_name).name_d3m
    download_d3m_dataset(d3m_dataset)

    problem_doc_path = d3m_dataset + '/SCORE/problem_TEST/problemDoc.json'
    with open(problem_doc_path) as f:
        problem_doc = json.load(f)

    learning_data_path = d3m_dataset + '/SCORE/dataset_TEST/tables/learningData.csv'
    X = pd.read_csv(learning_data_path, index_col=0)
    del X[problem_doc['inputs']['data'][0]['targets'][0]['colName']]

    y = pd.read_csv(d3m_dataset + '/SCORE/targets.csv', index_col=0)

    metric = problem_doc['inputs']['performanceMetrics'][0]['metric']

    # Cleanup
    shutil.rmtree(d3m_dataset)

    return X.values, y.values.ravel(), metric, problem_doc
