# coding=utf-8
import requests
import time

from flamp_vk.tables import VkInfoTable, FlampExpertsTable
from model import session_scope

VK_FIELDS = [
    u'sex', u'bdate', u'city', u'country',
    u'photo_50', u'photo_100', u'photo_200_orig', u'photo_200',
    u'photo_400_orig', u'photo_max', u'photo_max_orig', u'photo_id',
    u'online', u'online_mobile', u'domain', u'has_mobile', u'contacts',
    u'connections', u'site', u'education', u'universities', u'schools',
    u'can_post', u'can_see_all_posts', u'can_see_audio',
    u'can_write_private_message', u'status', u'last_seen',
    # u'common_count', # кол-во общих пользователей, видимо нужно
    # зарегистрироваться чтоб использовать это поле
    u'relation', u'relatives', u'counters', u'screen_name', u'maiden_name',
    u'timezone', u'occupation,activities', u'interests', u'music', u'movies',
    u'tv', u'books', u'games', u'about', u'quotes', u'personal',
    u'friend_status', u'military', u'career'
]


def _get_vk_url_by_id(id_, fields=VK_FIELDS):
    return u'https://api.vk.com/method/users.get?user_ids={}&name_case=nom&fields={}&v=5.42'\
        .format(id_, u','.join(fields))


def _get_vk_info(id_):
    return requests.get(_get_vk_url_by_id(id_)).content


def _get_user_id(vk_link):
    return vk_link.split('/')[-1]

if __name__ == "__main__":
    with session_scope() as sess:
        experts_vk_links = [
            (id_, _get_user_id(vk_link)) for id_, vk_link in
            sess.query(
                FlampExpertsTable.id_, FlampExpertsTable.vk_url
            ).outerjoin(
                VkInfoTable, VkInfoTable.id_ == FlampExpertsTable.id_
            ).filter(
                VkInfoTable.id_ == None
            ).filter(
                FlampExpertsTable.vk_url != None
            ).all()
        ]

    for id_, vk_id in experts_vk_links:
        print id_, vk_id
        vk_info = _get_vk_info(vk_id)
        with session_scope() as sess:
            sess.add(VkInfoTable(id_=id_, vk_id=vk_id,
                                 vk_json=vk_info.decode('utf8')))
        time.sleep(0.2)
