from model import get_dict
from tables import VkFeatures


def to_features(dict_):
    new_dict = dict()
    for key in ['age', 'occupation_type', 'photos_count', 'groups_count',
                'friends_count', 'followers_count', 'subscriptions_count',
                'gifts_count', 'life_main', 'political', 'relation', 'alcohol',
                'smoking', 'sex', 'people_main']:
        new_dict[key] = dict_[key]
    return new_dict


def get_features(ids=None):
    dict_fields = get_dict(VkFeatures)

    features_dict = {}
    for dict_ in dict_fields:
        if ids is not None and dict_['id_'] not in ids:
            continue
        features = to_features(dict_)
        features_dict[dict_['id_']] = features
    return features_dict


if __name__ == "__main__":
    from model import connect

    connect()
    f = get_features()

    print '\n'.join(map(str, f.items()[:100]))
