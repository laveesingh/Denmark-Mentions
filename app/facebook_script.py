# -*- coding: utf-8 -*-

from __future__ import print_function
import requests
import sys
import os
import time
import json
import threading
import datetime
import random
from pprint import pprint

from app.models import Fbcomment, Fbpost

from fb_pages_list import dump_to_file


HOST = 'graph.facebook.com'
pages_object = {}

if os.path.isfile('fb_logs.log'):
    with open('logs.log', 'a') as f:
        fb_logs = open('fb_logs.log', 'r').read()
        timestamp = datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        msg_timestamp = 'another session starts: %s' % timestamp
        f.write('%s\n%s' % (msg_timestamp, fb_logs))

f = open('fb_logs.log', 'w', 0)

def log(msg):
    print(msg, file=f)

def inline_log(msg):
    print(msg, end=' ', file=f)


def scrape_facebook(access_token):
    print('initiated facebook scraping')
    log('facebook started: %s' % datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))
    pages_list = load_pages_list()
    random.shuffle(pages_list)
    log('%d pages to be scraped' % len(pages_list))
    for page_id in pages_list:
        fetch_page_object(page_id, access_token)


def load_pages_list():
    if os.path.isfile('fb_pages_list.json'):
        pass
    else:
        dump_to_file()
    json_data = open('fb_pages_list.json', 'r').read()
    store = json.loads(json_data)
    return store['fb_pages_list']


def fetch_page_object(page_id, access_token):
    inline_log('^page')
    get_url = 'https://%s/v2.10/%s?access_token=%s&fields=posts{comments{'\
            'created_time,from,message},created_time,message},name' %\
            (HOST, str(page_id), access_token)
    response = requests.get(get_url)
    page_object = json.loads(response.content)
    page_name = page_object.get('name')
    pages_object[page_id] = {
        'page_name': page_name,
        'posts': {}
    }
    try:
        post_objects = page_object.get('posts').get('data')
        extract_posts_content(post_objects, pages_object[page_id]['posts'], page_name)
    except:
        pass



def extract_posts_content(post_objects, posts_object, page_name):
    for post in post_objects:
        post_id = post.get('id')
        post_content = post.get('message')
        timestamp = post.get('created_time')
        if not post_content:
            continue
        posts_object[post_id] = {
            'id': post_id,
            'message': post_content,
            'timestamp': timestamp,
            'page_name': page_name,
            'comments': {}
        }
        inline_log('>')
        qset = Fbpost.objects.filter(timestamp=timestamp, message=post_content)
        if qset:
            instance = qset.first()
            instance.post_id = post_id
            instance.save()
            inline_log('^')
            continue
        
        inserted = insert_fbpost(
            post_id=post_id,
            message=post_content,
            pagename=page_name,
            timestamp=timestamp
        )
        if inserted:
            inline_log('|')
        else:
            inline_log('<')
        extract_comments(post, posts_object[post_id]['comments'])
    inline_log('page$')


def extract_comments(post_object, comments_object):
    if post_object.get('comments') is None or\
            post_object.get('comments').get('data') is None:
        return
    for comment in post_object.get('comments').get('data'):
        comment_id = comment.get('id')
        comments_object[comment_id] = {
            'id': comment_id,
            'message': comment.get('message'),
            'user': comment.get('from').get('name'),
            'timestamp': comment.get('created_time')
        }

        inline_log('>')
        qset = Fbcomment.objects.filter(timestamp=comment.get('created_time'), message=comment.get('message'))
        if qset:
            instance = qset.first()
            instance.comment_id = comment_id
            instance.save()
            inline_log('^')
            continue
        inserted = insert_fbcomment(
            comment_id=comment.get('id'),
            message=comment.get('message'),
            username=comment.get('from').get('name'),
            timestamp=comment.get('created_time')
        )
        if inserted:
            inline_log('|')
        else:
            inline_log('<')


def insert_fbcomment(comment_id, message, username, timestamp, retry=0):
    try:
        Fbcomment.objects.create(
            comment_id=comment_id,
            message=message,
            username=username,
            timestamp=timestamp
        )
        return True
    except Exception as e:
        time.sleep(.1)
        if retry > 5:
            return False
        return insert_fbcomment(message, username, timestamp, retry+1)


def insert_fbpost(post_id, message, pagename, timestamp, retry=0):
    try:
        Fbpost.objects.create(
            post_id=post_id,
            message=message,
            pagename=pagename,
            timestamp=timestamp
        )
        return True
    except Exception as e:
        time.sleep(.1)
        if retry > 5:
            return False
        return insert_fbpost(message, pagename, timestamp, retry+1)
