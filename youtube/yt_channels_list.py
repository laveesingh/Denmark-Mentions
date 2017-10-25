from __future__ import print_function
import sys
import requests
import time
from bs4 import BeautifulSoup as Soup
import json


def log(msg):
    time.sleep(.5)
    print(msg, file=sys.stderr)

def inline_log(msg):
    time.sleep(.5)
    print(msg, file=sys.stderr, end='\r')

def yt_channels_list_util(url):
    '''takes a url and returns a list of yt_channel_id's'''
    inline_log('fetching url:%s........' % url)
    try:
        response = requests.get(url).content
    except:
        return []
    inline_log('done!!!')
    soup = Soup(response, 'html.parser')
    table = soup.find('table', attrs={'class': 'brand-table-list'})
    rows = [tr for tr in table.findAll('tr') if not tr.get('class') or (tr.get('class')[0] != 'replace-with-show-more')]
    channel_list = []
    inline_log('fetching list of channels')
    for row in rows:
        anchor = row.find('td', attrs={'class': 'name'}).find('div', attrs={'class': 'item'}).find('a')
        link = anchor.get('href')
        channel_id = link.split('/')[-1].split('-')[0]
        channel_list.append(channel_id)
    return channel_list


def yt_channels_list():
    '''fetches 400 long list of yt_channel_id's from denmark'''
    url_format = 'https://www.socialbakers.com/statistics/youtube/channels/denmark/page-%d-%d'
    channel_list = []
    for i in xrange(1, 42, 5):
        url = url_format % (i, i+4)
        channel_list.extend(yt_channels_list_util(url))
    return channel_list


def dump_to_file():
    '''writes 1000 long list of fb_page_id's from denmark to a file'''
    channels_list = yt_channels_list()
    log("channels found: %d" % len(channels_list))

    py_object = dict(
            yt_channels_list=channels_list
            )
    json_data = json.dumps(py_object)
    with open('yt_channels_list.json', 'w') as f:
        f.write(json_data)


if __name__ == '__main__':
    dump_to_file()

