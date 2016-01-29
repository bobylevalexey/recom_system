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


def get_vk_users_features(ids=None):
    dict_fields = get_dict(VkFeatures)
    features_dict = {
        dict_['id_']: to_features(dict_)
        for dict_ in dict_fields if ids is None or dict_['id_'] in ids
    }
    return features_dict


if __name__ == "__main__":
    from model import connect
    from sklearn.feature_extraction import DictVectorizer
    connect()
    # f = get_vk_users_features()

    d = DictVectorizer()
    d.fit_transform([{'1': 43, '2': 12}])
    print d.get_feature_names()
    d.fit_transform([{'4': 43, '5': 12}])
    print d.get_feature_names()
    # print '\n'.join(map(str, f.items()[:100]))
