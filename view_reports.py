from copy import deepcopy


def filter_by_key(results, key, val):
    return filter(lambda x: x[key] == val, results)


def get_max_min_avg(results, key):
    new_results = []
    key_sum = 0
    attempts_num = 0
    max_key_val = 0
    min_key_val = 1
    for dict_ in reversed(results):
        attempt_idx = dict_['attempt_idx']
        attempts_num += 1
        key_val = dict_[key]
        key_sum += key_val
        if key_val > max_key_val:
            max_key_val = key_val
        if key_val < min_key_val:
            min_key_val = key_val
        if attempt_idx == 1:
            new_dict = deepcopy(dict_)
            new_dict.pop('attempt_idx')
            new_dict.update({
                '{}_avg'.format(key): key_sum / attempts_num,
                'max_{}'.format(key): max_key_val,
                'min_{}'.format(key): min_key_val,
            })
            max_key_val = 0
            min_key_val = 1
            new_results.append(new_dict)
            attempts_num = 0
            key_sum = 0
    return new_results


def view_results(results, format_str, aggr_by=None, sort_by=None, desc=False):
    if aggr_by:
        results = get_max_min_avg(results, aggr_by)
    if sort_by:
        results = sorted(results, key=lambda x: x[sort_by], reverse=desc)
    for dict_ in results:
        print format_str.format(orig_dict=dict_, **dict_)
