import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Compile best results for ATM and OpenML.')
parser.add_argument('-r', '--runtype', type=str, choices=['gp', 'grid'], default='gp',
                     help='Which ATM run to use (gp or grid).')
parser.add_argument('-e', '--equalval', type=float, default=0.0001,
                     help='Maximum value to consider being an equal number.')
parser.add_argument('-u', '--outprefix', type=str, default='results',
                     help='File prefix used by compile_results.py (gp or grid will be automatically appended).')
args = parser.parse_args()

run_type = args.runtype

effectively_same_value = args.equalval

dataset_results_filename = '{}_{}.csv'.format(args.outprefix, run_type)
print dataset_results_filename

data = pd.read_csv(dataset_results_filename)

### cv

openml_beats_cv = data.loc[pd.notnull(data['openml_performance_increase_cv'])]
openml_beats_cv.reset_index(drop=True, inplace=True)
openml_beats_cv = openml_beats_cv.loc[pd.isnull(openml_beats_cv['atm_performance_increase_cv'])]
openml_beats_cv.reset_index(drop=True, inplace=True)

print 'Best F1 in the first 1000 OpenML runs is better than the best ATM cv (occurs {} of {} times):'.format(len(openml_beats_cv.index), len(data.index))
print '\tAverage time to achieve best performance in first 1000 OpenML: {} days'.format(openml_beats_cv['openml_time_to_best_f1'].mean()/float(86400))
print '\tAverage F1 increase over ATM: {}'.format(openml_beats_cv['openml_performance_increase_cv'].mean())

atm_cv_beats_openml = data.loc[pd.notnull(data['atm_performance_increase_cv'])]
openml_beats_cv.reset_index(drop=True, inplace=True)
atm_cv_beats_openml = atm_cv_beats_openml.loc[pd.isnull(atm_cv_beats_openml['openml_performance_increase_cv'])]
atm_cv_beats_openml.reset_index(drop=True, inplace=True)

print 'Best ATM cv F1 is better than best F1 in the first 1000 OpenML (occurs {} of {} times):'.format(len(atm_cv_beats_openml.index), len(data.index))
print '\tAverage time to attempt first 1000 OpenML: {} days'.format(atm_cv_beats_openml['openml_total_time'].mean()/float(86400))
print '\tAverage F1 increase over OpenML: {}'.format(atm_cv_beats_openml['atm_performance_increase_cv'].mean())

print 'Best ATM cv and Best OpenML in the first 1000 tie (F1 within 0.0001) {} times'.format(len(data.index)-len(openml_beats_cv.index)-len(atm_cv_beats_openml.index))


### test

openml_beats_test = data.loc[pd.notnull(data['openml_performance_increase_test'])]
openml_beats_test.reset_index(drop=True, inplace=True)
openml_beats_test = openml_beats_test.loc[pd.isnull(data['atm_performance_increase_test'])]
openml_beats_test.reset_index(drop=True, inplace=True)

print '\nBest F1 in the first 1000 OpenML runs is better than the best ATM test (occurs {} of {} times):'.format(len(openml_beats_test.index), len(data.index))
print '\tAverage time to achieve best performance in first 1000 OpenML: {} days'.format(openml_beats_test['openml_time_to_best_f1'].mean()/float(86400))
print '\tAverage F1 increase over ATM: {}'.format(openml_beats_test['openml_performance_increase_test'].mean())

atm_test_beats_openml = data.loc[pd.notnull(data['atm_performance_increase_test'])]
atm_test_beats_openml.reset_index(drop=True, inplace=True)
atm_test_beats_openml = atm_test_beats_openml.loc[pd.isnull(atm_test_beats_openml['openml_performance_increase_test'])]
atm_test_beats_openml.reset_index(drop=True, inplace=True)

print 'Best ATM test F1 is better than best F1 in the first 1000 OpenML (occurs {} of {} times):'.format(len(atm_test_beats_openml.index), len(data.index))
print '\tAverage time to attempt first 1000 OpenML: {} days'.format(atm_test_beats_openml['openml_total_time'].mean()/float(86400))
print '\tAverage F1 increase over OpenML: {}'.format(atm_test_beats_openml['atm_performance_increase_test'].mean())



print 'ATM test and OpenML tie (F1 within 0.0001) {} times'.format(len(data.index)-len(openml_beats_test.index)-len(atm_test_beats_openml.index))