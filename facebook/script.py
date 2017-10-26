from __future__ import print_function
import requests
import sys
import os
import json
from pprint import pprint

from fb_pages_list import dump_to_file


HOST = 'graph.facebook.com'
access_token = 'EAACEdEose0cBAJfm0x24raYJ0xJ0VBZBIbWvuGzqNNZAvltIGZBuTtMuZAW6Bb8gmfWGPFbIRTglpCZC6fu5e9IwnATZCKss8qM7k4ZA4pJKZC6vxvE13avkrmt6BQ855tDPZCeZA5EqUv8VO4uI2xA0O5UmQmTiyDZAbY1ZBocBY7wyyFOaLb9P5zOiYAalm3ek1mYZD'


def log(msg):
    print(msg, file=sys.stderr)


def load_pages_list():
    if os.path.isfile('fb_pages_list.json'):
       pass
    else:
        dump_to_file('https://www.socialbakers.com/statistics/facebook/pages/total/denmark/page-%d-%d/')
    json_data = open('fb_pages_list.json', 'r').read()
    store = json.loads(json_data)
    return store['fb_pages_list']


def post_list(page_id):
    url = 'https://%s/v2.10/%s?access_token=%s&fields=posts{comments}' % (HOST, str(page_id), access_token)
    log(  'requesting...' )
    response = requests.get(url)
    log(  'done!' )
    post_json = response.content
    post_objects = json.loads(post_json)['posts']['data']
    return post_objects

pages_list = load_pages_list()
first_page = pages_list[0]
posts = post_list(first_page)
pprint(posts[0])
