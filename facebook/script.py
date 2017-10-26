from __future__ import print_function
import requests
import sys
import os
import json
from pprint import pprint

from fb_pages_list import dump_to_file


HOST = 'graph.facebook.com'
access_token = 'EAACEdEose0cBAIahFKRJ4DAFyJ70bz6Kosi762GnK3n1JMlMGV7LELPiE1RJ7elK6G1ZAzBc81Mp6qDFw447ayoHYs1l3DZCXz4hTc20NaGvk4vEgMGpDMqtgUwjlKWBChZAjPmlAfeU5RAbVa959YktWfxPPmhccP38xwZBVsVKnOX61Ar57MWyHIDfNOYZD'


def log(msg):
    print(msg, file=sys.stderr)


def load_pages_list():
    if os.path.isfile('fb_pages_list.json'):
        log("found json for pages list!")
    else:
        log("fetching json for pages list...")
        dump_to_file('https://www.socialbakers.com/statistics/facebook/pages/total/denmark/page-%d-%d/')
        log("done!")
    json_data = open('fb_pages_list.json', 'r').read()
    store = json.loads(json_data)
    return store['fb_pages_list']


def fetch_page_object(page_id):
    url = 'https://%s/v2.10/%s?access_token=%s&fields=posts{comments{created_time,from,message},created_time,message},name' % (HOST, str(page_id), access_token)
    log(  'requesting for page_id:%s ...' % str(page_id) )
    response = requests.get(url)
    log(  'done!' )
    post_json = json.loads(response.content)
    page_name = post_json.get('name')

    try:
        post_objects = post_json.get('posts').get('data')
        return dict(
                post_objects=post_objects,
                page_name=page_name
            )
    except:
        return {'post_objects':[], 'page_name':''}


def fetch_post_content(post_obj, page_name):
    content = post_obj.get('message')
    timestamp = post_obj.get('created_time')
    return dict(
        content=content,
        page_name=page_name,
        timestamp=timestamp
    )
    

def fetch_post_comments_list(post_obj, page_name):
    post_content = post_obj.get('message')
    post_timestamp = post_obj.get('created_time')
    comment_list = []
    try:
        for comment in post_obj.get('comments').get('data'):
            comment_list.append({
                'post_content': post_content,
                'post_timestamp': post_timestamp,
                'page_name': page_name,
                'message': comment.get('message'),
                'user': comment.get('from').get('name'),
                'timestamp': comment.get('created_time')
            })
        return comment_list
    except:
        return []


if __name__ == '__main__':
    pages_list = load_pages_list()
    post_content_list = []
    post_comments_list = []

    PG_CNT = 0
    
    for page_id in pages_list:
        page_object = fetch_page_object(page_id)
        post_objects = page_object.get('post_objects')
        page_name = page_object.get('page_name')
        for post_object in post_objects:
            post_content_list.append(fetch_post_content(post_object, page_name))
            post_comments_list.extend(fetch_post_comments_list(post_object, page_name))
        PG_CNT += 1
        if PG_CNT > 2:
            break

