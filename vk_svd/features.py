from datetime import date

from sklearn.feature_extraction import DictVectorizer

from model import get_dict
from tables import VkFeatures


def _get_age(born):
    init_date = date(year=2016, month=1, day=1)
    return init_date.year - born.year - \
           ((init_date.month, init_date.day) < (born.month, born.day))


def _to_features(dict_):
    new_dict = dict()
    id_ = dict_['id_']
    new_dict['age'] = _get_age(dict_['bdate']) \
        if dict_['bdate'] is not None else None
    for new_key, def_dict, old_key in \
            [
                ('people_main', VkFeatures.PEOPLE_MAIN, 'people_main'),
                ('sex', VkFeatures.SEX, 'sex'),
                ('political', VkFeatures.POLIT, 'political'),
                ('relation', VkFeatures.RELATION, 'relation'),
                ('alcohol', VkFeatures.ALCO, 'alcohol'),
                ('smoking', VkFeatures.SMOKE, 'smoking'),
                ('life_main', VkFeatures.LIFE_MAIN, 'life_main'),
            ]:
        new_dict[new_key] = def_dict.get(dict_[old_key])
    for key in ['occupation_type', 'photos_count', 'groups_count',
                'friends_count', 'followers_count', 'subscriptions_count',
                'gifts_count']:
        new_dict[key] = dict_[key]
    return id_, new_dict


def get_features(ids=None):
    dict_fields = get_dict(VkFeatures)

    features_dicts = []
    features_ids = []
    for dict_ in dict_fields:
        if ids is not None and dict_['id_'] not in ids:
            continue
        id_, features = _to_features(dict_)
        features_ids.append(id_)
        features_dicts.append(features)
    return features_ids, features_dicts


if __name__ == "__main__":
    from model import connect

    connect()
    f = get_features()
    print '\n'.join(map(str, f[0][:100]))
    print '\n'.join(map(str, f[1][:100]))
