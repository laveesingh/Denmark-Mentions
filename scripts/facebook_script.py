# -*- coding: utf-8 -*-

from __future__ import print_function
import requests
import json
import datetime
import random

from app.models import Fbcomment, Fbpost

HOST = 'graph.facebook.com'
f = open('fb.log', 'w', 0)

def log(msg):
    print(msg, file=f)

def inline_log(msg):
    print(msg, end=' ', file=f)


def scrape_facebook(access_token):
    log('facebook scraping started: %s' %\
            datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))
    pages_list = json.loads(
            open('archive/fb_pages_list.json', 'r').read()).get('fb_pages_list')
    random.shuffle(pages_list)
    log('%d facebook pages to be scraped' % len(pages_list))
    for page_id in pages_list:
        get_url = 'https://%s/v2.10/%s?access_token=%s&fields=posts{comments{'\
                'created_time,from,message},created_time,message},name' %\
                (HOST, str(page_id), access_token)
        page_object = json.loads(requests.get(get_url).content)
        page_name = page_object.get('name')
        if not page_object.get('posts'):
            continue
        post_objects = page_object.get('posts').get('data')
        for post in post_objects:
            if not post: continue
            post_id = post.get('id')
            post_content = post.get('message')
            if not post_content: continue
            timestamp = post.get('created_time')
            query_set = Fbpost.objects.filter(timestamp=timestamp, message=post_content)
            if query_set:
                try:
                    instance = query_set.first()
                    instance.post_id = post_id
                    instance.page_id = page_id
                    instance.save()
                    inline_log('-+')
                except:
                    inline_log('-?')
                continue
            try:
                Fbpost.objects.create(
                    page_id=page_id,
                    post_id=post_id,
                    message=post_content,
                    pagename=page_name,
                    timestamp=timestamp
                )
                inline_log('++')
            except Exception as e:
                # inline_log('+?')
                log(e)
            if post.get('comments') is None or\
                    post.get('comments').get('data') is None:
                        continue
            for comment in post.get('comments').get('data'):
                comment_id = comment.get('id')
                message = comment.get('message')
                username = comment.get('from').get('name')
                user_id = comment.get('from').get('id')
                timestamp = comment.get('created_time')
                query_set = Fbcomment.objects.filter(timestamp=timestamp, message=message)
                if query_set:
                    try:
                        instance = query_set.first()
                        instance.page_id = page_id
                        instance.post_id = post_id
                        instance.user_id = user_id
                        instance.comment_id = comment_id
                        instance.save()
                        inline_log('-++')
                    except:
                        inline_log('-??')
                    continue
                try:
                    Fbcomment.objects.create(
                        page_id=page_id,
                        post_id=post_id,
                        user_id=user_id,
                        comment_id=comment_id,
                        username=username,
                        message=message,
                        timestamp=timestamp
                    )
                    inline_log('+++')
                except:
                    inline_log('+??')
