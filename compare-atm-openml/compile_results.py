import os
import datetime
import pandas as pd
import csv
import argparse

def calculate_time_to_atm_idx(results, idx):
    running_time = datetime.timedelta()
    for i in range(idx+1):
        row = results.loc[i]
        running_time += row['end_time'] - row['start_time']

    return running_time

def get_best_atm_performance(filepath):
    atm_results = pd.read_csv(filepath)
    atm_results['start_time'] = pd.to_datetime(atm_results['start_time'])
    atm_results['end_time'] = pd.to_datetime(atm_results['end_time'])
    atm_results = atm_results.sort_values('end_time')
    atm_results.reset_index(drop=True, inplace=True)

    cvs = atm_results['cv']
    stds = atm_results['std']
    tests = atm_results['test']

    best_cv = cvs.max()
    best_cv_idx = cvs.idxmax()
    # best_cv_std = stds.loc[best_cv_idx]
    # best_cv_test = tests.loc[best_cv_idx]

    best_test = tests.max()
    best_test_idx = tests.idxmax()
    # best_test_cv = cvs.loc[best_test_idx]
    # best_test_cv_std = stds.loc[best_test_idx]

    time_to_best_cv = calculate_time_to_atm_idx(atm_results, best_cv_idx)
    time_to_best_test = calculate_time_to_atm_idx(atm_results, best_test_idx)

    return best_cv, time_to_best_cv.total_seconds(), best_test, time_to_best_test.total_seconds()

def get_best_openml_performance(filepath, limit=500):
    openml_results = pd.read_csv(filepath)
    openml_results['Time'] = pd.to_datetime(openml_results['Time'])
    openml_results = openml_results.sort_values('Time')
    openml_results.reset_index(drop=True, inplace=True)
    openml_results = openml_results.head(n=limit)

    first_time = openml_results['Time'].iloc[0]
    last_time = openml_results['Time'].iloc[-1]

    best_f1 = openml_results['F_Measure'].max()
    best_f1_idx = openml_results['F_Measure'].idxmax()
    best_f1_time = openml_results['Time'].loc[best_f1_idx]

    time_to_best_f1 = best_f1_time - first_time
    total_time = last_time - first_time

    return best_f1, time_to_best_f1.total_seconds(), total_time.total_seconds()


def get_time_to_beat_atm(openml_filepath, best_f1):
    openml_results = pd.read_csv(openml_filepath)
    openml_results['Time'] = pd.to_datetime(openml_results['Time'])
    openml_results = openml_results.sort_values('Time')
    openml_results.reset_index(drop=True, inplace=True)

    first_time = openml_results['Time'].loc[0]

    for row in openml_results.iterrows():
        if row[1].get('F_Measure') > best_f1:
            return row[1].get('F_Measure'), (row[1].get('Time') - first_time).total_seconds()


parser = argparse.ArgumentParser(description='Compile best results for ATM and OpenML.')
parser.add_argument('-r', '--runtype', type=str, choices=['gp', 'grid'], default='gp',
                     help='Which ATM run to use (gp or grid).')
parser.add_argument('-o', '--openmldir', type=str, default='openml-results', help='Directory with OpenML results.')
parser.add_argument('-g', '--griddir', type=str, default='atm-results-grid-binary',
                     help='Directory with ATM Grid results')
parser.add_argument('-b', '--gpdir', type=str, default='atm-results-gpbandit-binary',
                     help='Directory with ATM GP+Bandit results')
parser.add_argument('-u', '--outprefix', type=str, default='results',
                     help='File prefix to save the output (gp or grid will be automatically appended).')
parser.add_argument('-c', '--didnamefile', type=str, default='openml-did-name-list.csv',
                     help='File which list OpenML did and dataset name.')
parser.add_argument('-e', '--equalval', type=float, default=0.0001,
                     help='Maximum value to consider being an equal number.')
args = parser.parse_args()

openml_dir = args.openmldir
grid_dir = args.griddir
gp_dir = args.gpdir

run_type = args.runtype

effectively_same_value = args.equalval

did_name_list = pd.read_csv(args.didnamefile)

dataset_results_filename = '{}_{}.csv'.format(args.outprefix, run_type)
with open(dataset_results_filename, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['did','name', 'best_cv', 'best_test', 'openml_best_f1', 'openml_time_to_best_f1',
                     'openml_performance_increase_cv', 'openml_performance_increase_test', 'openml_total_time',
                     'atm_performance_increase_cv', 'atm_performance_increase_test'])

    for row in did_name_list.iterrows():
        openml_filepath = os.path.join(openml_dir,'{}.csv'.format(row[1].get('did')))
        if run_type == 'grid':
            atm_filepath = os.path.join(grid_dir, row[1].get('name'))
        elif run_type == 'gp':
            atm_filepath = os.path.join(gp_dir, row[1].get('name'))
        else:
            raise Exception('unknown run type')

        if os.path.isfile(atm_filepath) and os.path.isfile(openml_filepath):
            best_cv, _, best_test, _ = get_best_atm_performance(filepath=atm_filepath)
            openml_best_f1, openml_time_to_best_f1, openml_total_time = get_best_openml_performance(filepath=openml_filepath)

            #openml better than cv
            if (openml_best_f1 - best_cv) > effectively_same_value:
                openml_performance_increase_cv = openml_best_f1 - best_cv
            else:
                openml_performance_increase_cv = float('nan')

            # openml better than test
            if (openml_best_f1 - best_test) > effectively_same_value:
                openml_performance_increase_test = openml_best_f1 - best_test
            else:
                openml_performance_increase_test = float('nan')

            #if cv better than openml
            if (best_cv - openml_best_f1) > effectively_same_value:
                atm_performance_increase_cv =  best_cv - openml_best_f1
            else:
                atm_performance_increase_cv = float('nan')

            # if test better than openml
            if (best_test - openml_best_f1) > effectively_same_value:
                atm_performance_increase_test = best_test - openml_best_f1
            else:
                atm_performance_increase_test = float('nan')

            writer.writerow([row[1].get('did'), row[1].get('name'), best_cv, best_test, openml_best_f1,
                             openml_time_to_best_f1, openml_performance_increase_cv, openml_performance_increase_test,
                             openml_total_time, atm_performance_increase_cv, atm_performance_increase_test])

