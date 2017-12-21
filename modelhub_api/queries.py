import pandas as pd
import os


class ClassifierInfo(object):
    def __init__(self):
        self.classifier_id = -1
        self.datarun_id = -1
        self.hyperparameters = []
        self.train_cv_metric = -1.0
        self.test_metric = -1.0

    def __repr__(self):
        return 'Classifier{}'.format(self.classifier_id)

    def __str__(self):
        return self.get_string_representation()

    def get_string_representation(self):
        str = ''

        str += 'Classifier - ID = {}\n'.format(self.classifier_id)
        str += '\t{} = {}\n'.format('Datarun ID', self.datarun_id)
        str += '\t{} = {}\n'.format('Train CV Metric', self.train_cv_metric)
        str += '\t{} = {}\n'.format('Test Metric', self.test_metric)
        str += '\tParameters:\n'
        for key,value in self.hyperparameters:
            str += '\t\t{} = {}\n'.format(key,value)

        return str


def get_datasets_info(csv_dir=None, n=None, method_ids=None):
    if not csv_dir:
        raise Exception('CSV directory must be given')

    if type(method_ids) is str:
        method_ids = [method_ids]

    datasets_filename = os.path.join(csv_dir, 'datasets.csv')
    datasets_table = pd.read_csv(datasets_filename)

    if method_ids:
        dataruns_filename = os.path.join(csv_dir, 'dataruns.csv')
        dataruns_table = pd.read_csv(dataruns_filename)

        hyperpartitions_filename = os.path.join(csv_dir, 'hyperpartitions.csv')
        hyperpartitions_table = pd.read_csv(hyperpartitions_filename)

        hyperpartitions_table = hyperpartitions_table[hyperpartitions_table.method.isin(method_ids)]
        datarun_ids = hyperpartitions_table.datarun_id.unique()

        dataruns_table = dataruns_table[dataruns_table.datarun_id.isin(datarun_ids)]
        datasets_ids = dataruns_table.dataset_id.unique()

        datasets_table = datasets_table[datasets_table.dataset_id.isin(datasets_ids)]
    if n:
        datasets_table = datasets_table.head(n=n)

    datasets_tuple_list = []
    for idx, row in datasets_table.iterrows():
        datasets_tuple_list.append((int(row.get('dataset_id')), row.get('name')))
    return datasets_tuple_list


def get_classifier_ids(csv_dir=None, n=None, dataset_ids=None, method_ids=None):
    if type(dataset_ids) is int:
        dataset_ids = [dataset_ids]

    if type(method_ids) is str:
        method_ids = [method_ids]

    classifier_filename = os.path.join(csv_dir, 'classifiers.csv')
    classifier_table = pd.read_csv(classifier_filename)

    classifier_table = classifier_table[classifier_table.status != 'errored']

    if method_ids:
        hyperpartitions_filename = os.path.join(csv_dir, 'hyperpartitions.csv')
        hyperpartitions_table = pd.read_csv(hyperpartitions_filename)

        hyperpartitions_table = hyperpartitions_table[hyperpartitions_table.method.isin(method_ids)]

        classifier_table = classifier_table[classifier_table.hyperpartition_id.isin(
                                            hyperpartitions_table.hyperpartition_id.unique())]

    if dataset_ids:
        dataruns_filename = os.path.join(csv_dir, 'dataruns.csv')
        dataruns_table = pd.read_csv(dataruns_filename)

        dataruns_table = dataruns_table[dataruns_table.dataset_id.isin(dataset_ids)]
        datarun_ids = dataruns_table.datarun_id.unique()

        classifier_table = classifier_table[classifier_table.datarun_id.isin(datarun_ids)]

    if n:
        classifier_table = classifier_table.head(n=n)

    classifier_id_list = []
    for idx, row in classifier_table.iterrows():
        classifier_id_list.append(int(row.classifier_id))

    return classifier_id_list


def get_classifier_details(csv_dir=None, classifier_ids=None):
    classifier_structs = []

    if classifier_ids:
        classifier_filename = os.path.join(csv_dir, 'classifiers.csv')
        classifier_table = pd.read_csv(classifier_filename)

        if (type(classifier_ids) == list):
            for classifier_id in classifier_ids:
                row = classifier_table[classifier_table.classifier_id == classifier_id].squeeze()
                classifier_structs.append(get_classifier_struct(row))

        if (type(classifier_ids) == int):
            classifier_structs = get_classifier_struct(classifier_ids)

    return classifier_structs


def get_classifier_struct(row):
    struct = ClassifierInfo()

    struct.classifier_id = row['classifier_id']
    struct.datarun_id = row['datarun_id']
    struct.train_cv_metric = row['cv_judgment_metric']
    struct.test_metric = row['test_judgment_metric']

    parameter_pairs = row['hyperparameter_values'].split(';')
    for parameter_pair in parameter_pairs:
        if len(parameter_pair) > 0: #ignore empty strings
            items = parameter_pair.split(':')
            struct.hyperparameters.append((items[0], items[1]))

    return struct
