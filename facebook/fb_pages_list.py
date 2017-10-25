import requests
import time
from bs4 import BeautifulSoup as Soup
import json




def fb_pages_list_util(url):
    '''takes a url and returns a list of fb_page_id's'''
    try:
        response = requests.get(url).content
    except:
        return []
    soup = Soup(response, 'html.parser')
    table = soup.find('table', attrs={'class': 'brand-table-list'})
    rows = [tr for tr in table.findAll('tr') if not tr.get('class') or (tr.get('class')[0] != 'replace-with-show-more')]
    page_list = []
    for row in rows:
        anchor = row.find('td', attrs={'class': 'name'}).find('div', attrs={'class': 'item'}).find('a')
        link = anchor.get('href')
        page_id = link.split('/')[-1].split('-')[0]
        page_list.append(page_id)
    return page_list


def fb_pages_list():
    '''fetches 1000 long list of fb_page_id's from denmark'''
    url_format = 'https://www.socialbakers.com/statistics/facebook/pages/total/denmark/page-%d-%d/'
    page_list = []
    for i in xrange(1, 97, 5):
        print 'fetching from %d to %d' % (i, i+4)
        url = url_format % (i, i+4)
        page_list.extend(fb_pages_list_util(url))
    return page_list


def dump_to_file():
    '''writes 1000 long list of fb_page_id's from denmark to a file'''
    page_list = fb_pages_list()
    print "pages list length:", len(page_list)
    py_object = dict(
            fb_pages_list=page_list
            )
    json_data = json.dumps(py_object)
    with open('fb_pages_list.json', 'w') as f:
        f.write(json_data)


# if __name__ == '__main__':
    # dump_to_file(URL)

