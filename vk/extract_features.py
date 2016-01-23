import json
from datetime import datetime

from model import connect, get, insert
from tables import VkInfoTable, VkFeatures


def get_by_keys(dict_, *keys):
    try:
        ret = dict_
        for key in keys:
            ret = ret.get(key)
        return ret
    except (KeyError, AttributeError):
        return None


def get_vk_jsons():
    jsons = get(VkInfoTable, {}, all_=True)
    return {vk_user.id_: json.loads(vk_user.vk_json) for vk_user in jsons}


def create_user_fields(json_):
    info = json_['response'][0]
    try:
        bdate = datetime.strptime(get_by_keys(info, 'bdate'), '%d.%m.%Y').date()
    except (ValueError, TypeError):
        bdate = None
    res_dict = {
        'sex': get_by_keys(info, 'sex'),
        'bdate': bdate,
        'relation': get_by_keys(info, 'relation'),
        'occupation_type': get_by_keys(info, 'occupation', 'type'),
        'albums_count': get_by_keys(info, 'counters', 'albums'),
        'videos_count': get_by_keys(info, 'counters', 'videos'),
        'photos_count': get_by_keys(info, 'counters', 'photos'),
        'friends_count': get_by_keys(info, 'counters', 'friends'),
        'groups_count': get_by_keys(info, 'counters', 'groups'),
        'pages_count': get_by_keys(info, 'counters', 'pages'),
        'followers_count': get_by_keys(info, 'counters', 'followers'),
        'user_videos_count': get_by_keys(info, 'counters', 'user_videos'),
        'notes_count': get_by_keys(info, 'counters', 'notes'),
        'user_photos_count': get_by_keys(info, 'counters', 'user_photos'),
        'subscriptions_count': get_by_keys(info, 'counters', 'subscriptions'),
        'political': get_by_keys(info, 'personal', 'political'),
        'people_main': get_by_keys(info, 'personal', 'people_main'),
        'life_main': get_by_keys(info, 'personal', 'life_main'),
        'smoking': get_by_keys(info, 'personal', 'smoking'),
        'alcohol': get_by_keys(info, 'personal', 'alcohol'),
        'wall_comments': get_by_keys(info, 'wall_comments'),
        'can_post': get_by_keys(info, 'can_post'),
        'can_see_all_posts': get_by_keys(info, 'can_see_all_posts'),
        'can_see_audio': get_by_keys(info, 'can_see_audio'),
        'can_write_private_message': get_by_keys(info,
                                                 'can_write_private_message'),
        'can_send_friend_request': get_by_keys(info, 'can_send_friend_request'),
        'activities': get_by_keys(info, 'activities'),
        'interests': get_by_keys(info, 'interests'),
        'music': get_by_keys(info, 'music'),
        'movies': get_by_keys(info, 'movies'),
        'tv': get_by_keys(info, 'tv'),
        'books': get_by_keys(info, 'books'),
        'games': get_by_keys(info, 'games'),
        'about': get_by_keys(info, 'about'),
        'quotes': get_by_keys(info, 'quotes'),
    }
    return res_dict

if __name__ == "__main__":
    connect()
    vk_users = get_vk_jsons()
    cols = create_user_fields(vk_users.values()[0])
    cols_counts = {col: 0 for col in cols}
    for u_id, user_dict in vk_users.iteritems():
        fields = create_user_fields(user_dict)
        insert(VkFeatures, **dict(id_=u_id, **fields))
        for field, val in fields.iteritems():
            if val is not None:
                cols_counts[field] += 1
