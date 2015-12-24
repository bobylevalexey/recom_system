import os
import pickle


def _get_object(file_name, dir_ = 'data'):
    with open(os.path.join(dir_, file_name)) as f:
        return pickle.load(f)

_EXPERTS_FILES = [
    'flamp_experts.pickle',
    'flamp_experts_1_51.pickle',
    'flamp_experts_51_101.pickle',
    'flamp_experts_101_151.pickle',
    'flamp_experts_151_201.pickle',
    'flamp_experts_201_251.pickle',
    'flamp_experts_251_301.pickle',
    'flamp_experts_301_351.pickle',
]

def get_experts():
    experts = []
    for exp_file in _EXPERTS_FILES:
        experts.extend(_get_object(exp_file))
    return experts

def view_experts():
    with open('data/flamp_experts.pickle') as f:
        experts = pickle.load(f)
    return experts



# experts = _get_object('flamp_experts_1_51.pickle')
experts = get_experts()
print len(experts)
print experts[0][:-1]#[s[1] for s in experts[:10]]
# print _get_object('flamp_experts_51_101.pickle')[:1]

# print view_experts()[10]



