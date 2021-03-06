import json
import traceback
from abc import ABCMeta, abstractmethod
from itertools import product
import time

from sklearn.cross_validation import train_test_split


class ParamsFinder(object):
    __metaclass__ = ABCMeta

    def __init__(self, attempts=10):
        self.attempts = attempts
        self.reports = None

    def iterate_over_params_dict(self, params_ranges_dict):
        params_names = params_ranges_dict.keys()
        params_ranges = params_ranges_dict.values()
        for params_values in product(*params_ranges):
            yield {p_name: p_val
                   for p_name, p_val in zip(params_names, params_values)}

    @abstractmethod
    def get_trainer(self, cls, options):
        pass

    @abstractmethod
    def train_model(self, train_data, test_data, model, trainer):
        return {}

    def find(self, data, trainer_cls, model_range, tr_params_ranges,
             static_params, dump_to=None, train_size=0.7):
        self.reports = []

        static_params = static_params or {}
        for model, model_info in model_range:
            for params in self.iterate_over_params_dict(tr_params_ranges):
                params.update(static_params)
                for attempt_idx in xrange(self.attempts):
                    print "next try: {}, {}, {}".format(model_info, attempt_idx,
                                                        params)
                    train_data, test_data = train_test_split(
                        data, train_size=train_size)
                    trainer = self.get_trainer(trainer_cls, params)
                    report = dict(params)
                    report['model'] = model_info
                    report['attempt_idx'] = attempt_idx
                    try:
                        start = time.time()
                        report.update(
                            self.train_model(train_data, test_data,
                                             model, trainer))
                        report['time'] = time.time() - start
                    except Exception:
                        report['error'] = traceback.format_exc()

                    print 'report', report
                    self.reports.append(report)
        if dump_to:
            self.dump_reports(dump_to)
        return self.reports

    def dump_reports(self, file_name):
        try:
            with open(file_name) as f:
                old_reports = json.load(f)
        except IOError:
            old_reports = []
        with open(file_name, 'w') as f:
            json.dump(old_reports + self.reports, f)
