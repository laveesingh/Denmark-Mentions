from __future__ import print_function
import requests
import sys
import os
import time
import json
import threading
from pprint import pprint

from fb_pages_list import dump_to_file


HOST = 'graph.facebook.com'
access_token = 'EAACEdEose0cBAB0OzZBZAj8QNXGBSt21BOny9jOvOMITflnK8H8ZBPd3WHgBShSGZCoOoJUMqTNsZCj528OqL8jfbIzZC98FqKvIcGZBWOy3NybZAycVDf2TYMDWlRZBd7HiA5DdoCwa3o1LEXUibwKShX3NRQpFNIyXQI4LkEsMZCt8wekfk0ZAGwCYkRVWU0Fo1EZD'

start_time = time.time()

def log(msg):
    print('.', end='', file=sys.stderr)


def load_pages_list():
    if os.path.isfile('fb_pages_list.json'):
        log("found json for pages list!")
    else:
        log("fetching json for pages list...")
        # log("couldn't find fb_pages_list.json listdir: %s" % str(os.listdir('.')))
        dump_to_file()
        log("done!")
    json_data = open('fb_pages_list.json', 'r').read()
    store = json.loads(json_data)
    return store['fb_pages_list']


def fetch_page_object(page_id, page_count):
    url = 'https://%s/v2.10/%s?access_token=%s&fields=posts{comments{created_time,from,message},created_time,message},name' % (HOST, str(page_id), access_token)
    log(  'requesting for page_id:%s ...' % str(page_id) )
    response = requests.get(url)
    log('request completed for page: %d' % page_count)
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


def store_to_lists(page_id, post_content_list, post_comments_list, page_count):
    page_object = fetch_page_object(page_id, page_count)
    post_objects = page_object.get('post_objects')
    page_name = page_object.get('page_name')
    for post_object in post_objects:
        post_content_list.append(fetch_post_content(post_object, page_name))
        post_comments_list.extend(fetch_post_comments_list(post_object, page_name))
    log("page scraped: %d, comments: %d, posts: %d, time: %f, active_threads: %d" % (page_count+1, len(post_comments_list), len(post_content_list), time.time()-start_time, threading.active_count()))



# if __name__ == '__main__':
def scrape_facebook():
    pages_list = load_pages_list()
    log("%d pages found" % len(pages_list))
    post_content_list = []
    post_comments_list = []
    page_count = 0
    for page_id in pages_list:
        threading.Thread(target=store_to_lists, args=(page_id, post_content_list, post_comments_list, page_count)).start()
        page_count += 1
    return dict(
        post_content_list=post_content_list,
        post_comments_list=post_comments_list
    )

# store = scrape_facebook()
# end_time = time.time()
# print ("time taken: %f seconds" % float(end_time - start_time))
