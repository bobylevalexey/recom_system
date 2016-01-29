# coding=utf-8
from math import ceil
import pickle
import traceback

import requests
import bs4


try:
    for ind in xrange(1, 501, 50):
        users = []
        for i in xrange(ind, ind + 50):
            print i
            cont = requests.get('http://ekaterinburg.flamp.ru/experts?page=' + str(i)).content
            soup = bs4.BeautifulSoup(cont, 'lxml')
            for user_div in soup.findAll('div', {'class': 'user'}):
                user_a = user_div.find('a', {'class': 'user-name'})
                user_name = user_a.find('span').text
                user_link = user_a['href']
                reviews = int(user_div.find('li', {'class': 'reviews-and-followers'}).find('span').text)
                user_link = '{}?limit={}'.format(user_link, int(ceil(reviews / 10.)) * 10)
                user_page = requests.get(user_link).content
                vk_span = bs4.BeautifulSoup(user_page, 'lxml').find('span', {'title': u'ВКонтакте'})
                if vk_span:
                    vk_link = vk_span.findNext('a')['href']
                else:
                    vk_link = None
                users.append((user_name, user_link, reviews, vk_link, user_page))
                print user_name, user_link, reviews, vk_link
        with open('data/flamp_experts_{}_{}.pickle'.format(ind, ind + 50), 'w') as f:
            pickle.dump(users, f)

except (KeyboardInterrupt,Exception) as e:
    print traceback.format_exc()
