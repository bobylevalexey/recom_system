import json
import os
from copy import deepcopy

from rs_config import DATA_DIR


def filter_by_feature(results, feature):
    return filter(lambda x: x['feature'] == feature, results)


def get_max_min_avg(results):
    new_results = []
    err_sum = 0
    attempts_num = 0
    max_err = 0
    min_err = 1
    for dict_ in reversed(results):
        attempt_idx = dict_['attempt_idx']
        attempts_num += 1
        err_sum += dict_['err']
        if dict_['err'] > max_err:
            max_err = dict_['err']
        if dict_['err'] < min_err:
            min_err = dict_['err']
        if attempt_idx == 1:
            new_dict = deepcopy(dict_)
            new_dict.pop('attempt_idx')
            new_dict.update({
                'err': err_sum / attempts_num,
                'max_err': max_err,
                'min_err': min_err,
            })
            max_err = 0
            min_err = 1
            new_results.append(new_dict)
            attempts_num = 0
            err_sum = 0
    return new_results

if __name__ == "__main__":

    with open(os.path.join(DATA_DIR, 'logistic_results.json')) as f:
        results = json.load(f)

    used_features = set()
    for dict_ in sorted(get_max_min_avg(results), key=lambda x: x['err']):
        if dict_['test_size'] < 20:
            continue
        if dict_['feature'] in used_features:
            continue
        used_features.add(dict_['feature'])
        print '{0:<16} {1:<16} {2:<16} {3:<16} {4:<2} {5:<2} {6}'.format(
            dict_['feature'], dict_['err'], dict_['min_err'],
            dict_['max_err'], dict_['min_marks'], dict_['test_size'],
            dict_
        )
