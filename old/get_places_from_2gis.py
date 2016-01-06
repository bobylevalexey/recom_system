# coding:utf8
import pickle
import requests
import time
import traceback

import bs4

import get_data

__author__ = 'alexey'


def get_all_cafe_links():
    all_refs = []
    for page in xrange(1, 121):
        print page
        resp = requests.get(
            'https://2gis.ru/ekaterinburg/search/Поесть/page/{}/zoom/11'.format(page))
        soup = bs4.BeautifulSoup(resp.content)
        refs = soup('a', {'class': 'mediaMiniCard__link'})
        all_refs.extend(ref['href'] for ref in refs)
        time.sleep(0.3)
    with open('backup/places_links.pickle', 'wb') as f:
        pickle.dump(all_refs, f)


def get_places_pages():
    refs = get_data.get_2gis_places_links()
    pages = []
    for i, ref in enumerate(refs):
        print i, ref
        full_ref = 'https://2gis.ru{}'.format(ref)
        about, reviews, discount = [None] * 3
        try:
            print 'about'
            about = requests.get(full_ref).content
        except :
            print traceback.format_exc()

        try:
            print 'reviews'
            ab_ref = full_ref.replace('about', 'reviews')
            about = requests.get(ab_ref).content
        except :
            print traceback.format_exc()

        try:
            print 'discount'
            dis_ref = full_ref.replace('about', 'discount')
            about = requests.get(dis_ref).content
        except :
            print traceback.format_exc()
        pages.append((ref, {'about': about, 'reviews': reviews, 'discount': discount}))
        time.sleep(0.3)
    with open('data/places_pages.pickle', 'wb') as f:
        pickle.dump(pages, f)

get_places_pages()
