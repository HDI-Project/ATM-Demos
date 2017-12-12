import os
import datetime
import pandas as pd
import csv

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

def get_best_openml_performance(filepath):
    openml_results = pd.read_csv(filepath)
    openml_results['Time'] = pd.to_datetime(openml_results['Time'])
    openml_results = openml_results.sort_values('Time')
    openml_results.reset_index(drop=True, inplace=True)

    first_time = openml_results['Time'].loc[0]

    best_f1 = openml_results['F_Measure'].max()
    best_f1_idx = openml_results['F_Measure'].idxmax()
    best_f1_time = openml_results['Time'].loc[best_f1_idx]

    time_to_best_f1 = best_f1_time - first_time

    return best_f1, time_to_best_f1.total_seconds()


def get_time_to_beat_atm(openml_filepath, best_f1):
    openml_results = pd.read_csv(openml_filepath)
    openml_results['Time'] = pd.to_datetime(openml_results['Time'])
    openml_results = openml_results.sort_values('Time')
    openml_results.reset_index(drop=True, inplace=True)

    first_time = openml_results['Time'].loc[0]

    for row in openml_results.iterrows():
        if row[1].get('F_Measure') > best_f1:
            return row[1].get('F_Measure'), (row[1].get('Time') - first_time).total_seconds()

openml_dir = 'openml-results'
grid_dir = 'atm-results-grid-binary'
gp_dir = 'atm-results-gpbandit-binary'

effectively_same_value = 0.0001

did_name_list = pd.read_csv('openml-did-name-list.csv')


with open('results.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(['did','name', 'gp_best_cv', 'gp_time_to_best_cv', 'gp_best_test', 'gp_time_to_best_test',
                     'grid_best_cv', 'grid_time_to_best_cv', 'grid_best_test', 'grid_time_to_best_test',
                     'openml_best_f1', 'openml_time_to_best_f1', 'openml_beat_atm_cv_f1_gp',
                     'openml_time_beat_atm_cv_gp', 'openml_beat_atm_cv_f1_grid', 'openml_time_beat_atm_cv_grid',
                     'openml_beat_atm_test_f1_gp', 'openml_time_beat_atm_test_gp', 'openml_beat_atm_test_f1_grid',
                     'openml_time_beat_atm_test_grid'])

    for row in did_name_list.iterrows():
        openml_filepath = os.path.join(openml_dir,'{}.csv'.format(row[1].get('did')))
        grid_filepath = os.path.join(grid_dir, row[1].get('name'))
        gp_filepath = os.path.join(gp_dir, row[1].get('name'))

        if os.path.isfile(gp_filepath) and os.path.isfile(grid_filepath) and os.path.isfile(openml_filepath):
            gp_best_cv, gp_time_to_best_cv, gp_best_test, gp_time_to_best_test = get_best_atm_performance(
                filepath=gp_filepath)
            grid_best_cv, grid_time_to_best_cv, grid_best_test, grid_time_to_best_test = get_best_atm_performance(
                filepath=grid_filepath)
            openml_best_f1, openml_time_to_best_f1 = get_best_openml_performance(filepath=openml_filepath)

            # compare openml and cv scores
            if openml_best_f1 - gp_best_cv > effectively_same_value:
                openml_beat_atm_cv_f1_gp, openml_time_beat_atm_cv_gp = get_time_to_beat_atm(openml_filepath=openml_filepath, best_f1=gp_best_cv)
            else:
                openml_beat_atm_cv_f1_gp = float('nan')
                openml_time_beat_atm_cv_gp = float('nan')

            if openml_best_f1 - grid_best_cv > effectively_same_value:
                openml_beat_atm_cv_f1_grid, openml_time_beat_atm_cv_grid = get_time_to_beat_atm(openml_filepath=openml_filepath, best_f1=grid_best_cv)
            else:
                openml_beat_atm_cv_f1_grid = float('nan')
                openml_time_beat_atm_cv_grid = float('nan')

            # compare openml and test scores
            if openml_best_f1 - gp_best_test > effectively_same_value:
                openml_beat_atm_test_f1_gp, openml_time_beat_atm_test_gp = get_time_to_beat_atm(openml_filepath=openml_filepath, best_f1=gp_best_test)
            else:
                openml_beat_atm_test_f1_gp = float('nan')
                openml_time_beat_atm_test_gp = float('nan')

            if openml_best_f1 - grid_best_test > effectively_same_value:
                openml_beat_atm_test_f1_grid, openml_time_beat_atm_test_grid = get_time_to_beat_atm(openml_filepath=openml_filepath, best_f1=grid_best_test)
            else:
                openml_beat_atm_test_f1_grid = float('nan')
                openml_time_beat_atm_test_grid = float('nan')

            writer.writerow([row[1].get('did'), row[1].get('name'), gp_best_cv, gp_time_to_best_cv, gp_best_test,
                             gp_time_to_best_test, grid_best_cv, grid_time_to_best_cv, grid_best_test,
                             grid_time_to_best_test, openml_best_f1, openml_time_to_best_f1, openml_beat_atm_cv_f1_gp,
                             openml_time_beat_atm_cv_gp, openml_beat_atm_cv_f1_grid, openml_time_beat_atm_cv_grid,
                             openml_beat_atm_test_f1_gp, openml_time_beat_atm_test_gp, openml_beat_atm_test_f1_grid,
                             openml_time_beat_atm_test_grid])
