# coding=utf-8
from bs4 import BeautifulSoup
import requests

from model import connect, get, update, get_dict
from tables import FlampExpertsTable


if __name__ == "__main__":
    connect()
    expert_ids = (dict_['id_']
                  for dict_ in get_dict(FlampExpertsTable, ['id_']))
    for idx, id_ in enumerate(expert_ids):
        print idx, id_
        exp = get(FlampExpertsTable, {'id_': id_})
        if exp.page.find(u'<em class="georgia">Её оценки</em>') != -1:
            sex = 'female'
        elif exp.page.find(u'<em class="georgia">Его оценки</em>') != -1:
            sex = 'male'
        else:
            sex = None
            print u'err! {} {}'.format(exp.id_, exp.flamp_url)
        print sex
        update(FlampExpertsTable, {'id_': id_}, {'sex': sex})
        # soup = BeautifulSoup(exp.page, 'lxml')
        # col2 = soup.find('div', {'class': 'content-col-2'})
        # for modbox in col2.findAll('div', {'class': 'modbox'}):
        #     em = modbox.find('em')
        #     if em is None:
        #         continue
        #     em_text = em.getText()
        #     if em_text.startswith(u'Её'):
        #         sex = 'female'
        #         break
        #     elif em_text.startswith(u'Его'):
        #         sex = 'male'
        #         break
        # else:
        #     sex = None
        #     print 'err! {} {}'.format(exp.id_, exp.flamp_url)
        #
        # print sex


