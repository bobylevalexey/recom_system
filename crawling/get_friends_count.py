import json

import requests

import time

from model import connect, get_dict, update
from tables import VkFeatures, VkInfoTable


def _get_friends_count(vk_id):
    url = 'https://api.vk.com/method/friends.get?user_id={}&v=5.44'.format(
        vk_id[2:]  # id123456 -> 123456
    )
    json_content = json.loads(requests.get(url).content)
    try:
        return json_content['response']['count']
    except Exception as e:
        print e, json_content

if __name__ == "__main__":
    connect()
    ids = get_dict(VkInfoTable, ('id_', 'vk_id'))
    fr_counts = {f['id_']: f['friends_count']
                 for f in get_dict(VkFeatures, ('id_', 'friends_count'))}
    for idx, id_dict in enumerate(ids):
        print idx + 1, id_dict
        if fr_counts[id_dict['id_']] is not None:
            print 'skiping'
            continue
        fr_count = _get_friends_count(id_dict['vk_id'])
        update(VkFeatures, {'id_': id_dict['id_']}, {'friends_count': fr_count})
