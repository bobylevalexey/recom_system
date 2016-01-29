import json
import os

from view_reports import view_results
from rs_config import DATA_DIR

if __name__ == "__main__":

    with open(os.path.join(DATA_DIR, 'ml_rsvd_params_report.json')) as f:
        results = json.load(f)

    view_results(
        results, '{test_err_avg:<16} {train_err:<16} {orig_dict}',
        aggr_by='test_err', sort_by='test_err', desc=False)
