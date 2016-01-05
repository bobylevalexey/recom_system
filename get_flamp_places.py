import traceback

import time
from bs4 import BeautifulSoup
import requests

from model import connect, insert, get, session_scope
from tables import FlampExpertsTable, FlampFirmsTable, FlampMarksTable


def _get_firm_id_from_url(url):
    return url.strip().split('?')[0].split('/')[-1]


def get_places_info_gen(flamp_expert_page):
    soup = BeautifulSoup(flamp_expert_page, 'lxml')
    rev_items = soup.find('div', {'id': 'reviews'}).findAll(
            'li', {'class': 'review-item'})
    for rev_it in rev_items:
        mark_url = rev_it.find('meta', {'itemprop': 'url'})['content']
        firm_url = rev_it.find('a', {'itemprop': 'url'})['href']
        mark = rev_it.find('span', {'itemprop': 'ratingValue'}).text
        yield {'id': _get_firm_id_from_url(firm_url),
               'mark': int(mark), 'url': firm_url, 'mark_url': mark_url}


def get_url(url):
    for _ in xrange(4):
        try:
            page = requests.get(url).content
            break
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise
            time.sleep(2)
            traceback.print_exc()
    else:
        raise RuntimeError('Flamp is busy')
    return page.decode('utf8')

if __name__ == "__main__":
    connect()

    i = 0
    with session_scope() as sess:
        user_ids = sess.query(FlampExpertsTable.id_).all()
    for user_tuple in user_ids:
        user_id = user_tuple[0]
        user = get(FlampExpertsTable, {'id_': user_id})
        print i, user.user_name, user_id
        i += 1
        for firm_dict in get_places_info_gen(user.page):
            firm_obj = get(FlampFirmsTable, {'flamp_id': firm_dict['id']})
            if firm_obj is None:
                time.sleep(0.5)
                page = get_url(firm_dict['url'])
                print 'inserting new object', firm_dict
                insert(FlampFirmsTable, flamp_id=firm_dict['id'].decode('utf8'),
                       page=page)
                firm_obj = get(FlampFirmsTable, {'flamp_id': firm_dict['id']})
            if get(FlampMarksTable, {'mark_url': firm_dict['mark_url']}) \
                    is None:
                insert(FlampMarksTable, expert_id=user_id, firm_id=firm_obj.id_,
                       mark=firm_dict['mark'],
                       mark_url=firm_dict['mark_url'].decode('utf8'))

    # user = get(FlampExpertsTable, {'id_': 30})
    # print list(get_places_info_gen(user.page))

