import requests
import csv
import os
import argparse
import traceback


def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_results(runid, apikey):
    result_dict = None

    url = 'https://www.openml.org/api/v1/json/run/{}?{}'.format(runid, apikey)

    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        if r.content:
            j = r.json()

            result_dict = dict()

            for result in (j['run']['output_data']['evaluation']):
                if 'value' in result:
                    result_dict[str(result['name'])] = float(result['value'])

    return result_dict


def get_tasks(dataid, apikey):
    task_list = []

    url = 'https://www.openml.org/api/v1/json/task/list/data_id/{}/type/1?api_key={}'.format(dataid, apikey)

    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        if r.content:
            j = r.json()
            for task in j['tasks']['task']:
                task_list.append(task['task_id'])

    return task_list


def get_runs(taskids, apikey, writer, max_num_runs=500, step=10000):
    runcount = 0

    for task in taskids:
        at_end = False
        offset = 0

        while not at_end:
            url = 'https://www.openml.org/api/v1/json/run/list/task/{}/limit/{}/offset/{}?api_key={}'.format(task, step,
                                                                                                             offset, apikey)
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                try:
                    if r.content:
                        j = r.json()

                        for run in j['runs']['run']:
                            result = get_results(runid=run['run_id'],
                                                 apikey=apikey)

                            try:
                                writer.writerow([run['run_id'],
                                                 run['upload_time'],
                                                 result['predictive_accuracy'],
                                                 result['f_measure'],
                                                 result['precision'],
                                                 result['recall']])
                            except Exception:
                                msg = traceback.format_exc()
                                print 'result skipped: {}'.format(msg)

                            runcount += 1

                            if (max_num_runs > 0) and (runcount % max_num_runs == 0):
                                return # reached max num_of_runs, so stop looking and return to main

                except Exception:
                    msg = traceback.format_exc()
                    print 'bad return: {}'.format(msg)

                offset += step
            else:
                at_end = True


parser = argparse.ArgumentParser(description='Download OpenML run results.')
parser.add_argument('-K', '--apikey', required=True, type=str,
                    help='OpenML API Key to use.')
parser.add_argument('-f', '--didfile', type=str, required=True,
                    help='Path to dataset id file.')
parser.add_argument('-d', '--outdir', type=str, default='openml',
                    help='Folder to store the output.')
parser.add_argument('-N', '--numruns', type=int, default=0,
                    help='Maximum number of runs to download for each dataset. 0 indicates no maximum -- download all runs.')
args = parser.parse_args()


with open(args.didfile, 'r') as id_file:
    dids = id_file.readlines()

ensure_directory(directory=args.outdir)

for counter, did in enumerate(dids):
    # convert from string to integer (also removes endline)
    did = int(did)

    tasks = get_tasks(dataid=did, apikey=args.apikey)

    dataset_output_filepath = os.path.join(args.outdir, '{}.csv'.format(did))
    with open(dataset_output_filepath, 'wb') as dataset_file:

        writer = csv.writer(dataset_file)
        writer.writerow(['Run ID', 'Time', 'Predictive_Accuracy', 'F_Measure',
                         'Precision', 'Recall'])

        get_runs(taskids=tasks, apikey=args.apikey, writer=writer,
                 max_num_runs=args.numruns)

    print '{} datasets processed'.format(counter)
