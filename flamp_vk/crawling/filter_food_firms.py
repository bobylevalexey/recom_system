# coding=utf-8
import config
from bs4 import BeautifulSoup

from flamp_vk.tables import FlampFirmsTable, FoodEkbFirms
from model import connect, iterate_over_table, update, insert


def _get_city(soup):
    try:
        return soup.find('input', {'id': 'search-where'})['value']
    except (AttributeError, TypeError):
        return None


def _get_category(soup):
    try:
        category_ref = soup.find(
            'ul', {'class': ['company-tags', 'inline-list', 'georgia']}
        ).find('a')['href']
        return category_ref[5:]
    except (AttributeError, TypeError):
        return None


def get_info_from_page(page):
    soup = BeautifulSoup(page, 'lxml')
    return {
        'category': _get_category(soup),
        'city': _get_city(soup)
    }


if __name__ == "__main__":
    connect()
    for firm_obj in iterate_over_table(FlampFirmsTable):
        info = get_info_from_page(firm_obj.page)
        update(FlampFirmsTable, {'id_': firm_obj.id_}, {
            'category_url': info['category'],
            'city': info['city']
        })
        print firm_obj.flamp_id, info['category'], info['city']
        if info['category'] in config.FOOD_CATEGORIES \
                and info['city'] == u'Екатеринбург':
            insert(FoodEkbFirms, food_pk=firm_obj.id_)
            print 'added to food ekb firms'

