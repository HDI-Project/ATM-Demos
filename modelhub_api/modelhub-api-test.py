import argparse
import queries as qr

parser = argparse.ArgumentParser(description='Explore ATM results.')
parser.add_argument('-r', '--runtype', type=str, choices=['gp', 'grid'], default='gp',
                     help='Which ATM run to use (gp or grid).')
args = parser.parse_args()

if args.runtype == 'gp':
    csv_dir = 'gp_csvs'
else:
    csv_dir = 'grid_csvs'


print '\nThese are 5 datasets in the ModelHub for which SVM & KNN have been applied:'

datasets = qr.get_datasets_info(csv_dir=csv_dir, n=5, method_ids= ['classify_svm', 'classify_knn'])
print '\t+{}+'.format('-'*41)
print '\t| {0: >3} | {1: <33} |'.format('ID', 'Dataset')
print '\t+{}+'.format('-'*41)
for dataset in datasets:
    print '\t| {0: >3} | {1: <33} |'.format(dataset[0],dataset[1])
print '\t+{}+'.format('-' * 41)



print '\nHere are some SVM & KNN results for dataset 2:'

classifier_ids = qr.get_classifier_ids(csv_dir=csv_dir, n = 5, dataset_ids = 2, method_ids= ['classify_svm', 'classify_knn'])
classifier_structs = qr.get_classifier_details(csv_dir=csv_dir, classifier_ids=classifier_ids)

print '\t|{}|'.format('-'*29)
print '\t| {0: >15} | {1: <9} |'.format('Classifier ID', 'Test Acc.')
print '\t|{}|'.format('-'*29)
for classifier_struct in classifier_structs:
    print '\t| {0: >15} | {1:9.2f} |'.format(classifier_struct.classifier_id,classifier_struct.test_metric)
print '\t|{}|'.format('-' * 29)

print '\nClassifier Details:\n'
for classifier_struct in classifier_structs:
    print classifier_struct