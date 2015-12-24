from collections import defaultdict
import pickle

import bs4

__author__ = 'alexey'


# with open('data/flamp_experts_1_51.pickle') as f:
#     experts = pickle.load(f)
#
# places = defaultdict(list)
# for name, link, revs, vk_link, page in experts:
#     if vk_link:
#         soup = bs4.BeautifulSoup(page, 'lxml')
#         for li in soup.findAll('li', {'class': 'review-item'}):
#             ref = li.find('a', {'class': 'link-short-list'})['href']
#             mark = li.find('span', {'itemprop': 'ratingValue'}).text
#             places[ref].append((link, mark, name))
#
# with open('data/flamp_places.pickle', 'w') as f:
#     pickle.dump(places, f)

with open('data/flamp_places.pickle') as f:
    places = pickle.load(f)

max_p = ''
max_revs = -1

for place in places:
    if len(places[place]) > max_revs:
        max_p = place
        max_revs = places[place]

top_places = sorted(places.iteritems(), key=lambda x: len(x[1]), reverse=True)

for p in top_places[:10]:
    print p[0]


