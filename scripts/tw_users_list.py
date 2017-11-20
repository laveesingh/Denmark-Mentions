import requests
import time
from bs4 import BeautifulSoup as Soup
import json


def tw_users_list_util(url):
    '''takes a url and returns a list of tw_user_id's'''
    try:
        response = requests.get(url).content
    except:
        return []
    soup = Soup(response, 'html.parser')
    table = soup.find('table', attrs={'class': 'brand-table-list'})
    rows = [tr for tr in table.findAll('tr') if not tr.get('class') or (tr.get('class')[0] != 'replace-with-show-more')]
    user_list = []
    for row in rows:
        anchor = row.find('td', attrs={'class': 'name'}).find('div', attrs={'class': 'item'}).find('a')
        link = anchor.get('href')
        user_id = link.split('/')[-1].split('-')[0]
        user_list.append(user_id)
    return user_list


def tw_users_list():
    '''fetches 570 long list of twitter user id's from denmark'''
    url_format = 'https://www.socialbakers.com/statistics/twitter/profiles/denmark/page-%d-%d/'
    user_list = []
    for i in xrange(1, 60, 5):
        print 'fetching from %d to %d' % (i, i+4)
        url = url_format % (i, i+4)
        user_list.extend(tw_users_list_util(url))
    return user_list


def dump_to_file():
    '''writes 1000 long list of tw_user_id's from denmark to a file'''
    user_list = tw_users_list()
    print "users list length:", len(user_list)
    py_object = dict(
            tw_users_list=user_list
            )
    json_data = json.dumps(py_object)
    with open('tw_users_list.json', 'w') as f:
        f.write(json_data)


if __name__ == '__main__':
    dump_to_file()

