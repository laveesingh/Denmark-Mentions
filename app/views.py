# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import threading
import time

from django.shortcuts import render
from django.http import HttpResponse

from facebook_script import scrape_facebook
from app.models import Ytcomment, Fbpost, Fbcomment, ObjectHash


def update(request):
    save_scraped_objects_to_db()
    return HttpResponse("something")


def search(request):
    data = reqeust.GET
    keywords = data['keywords'].split()
    comments = Fbcomment.objects.all()
    valid_comments = []
    for comment in comments:
        for keyword in keywords:
            if keyword in comment['message']:
                valid_comments.append(comment)
                break
    posts = Fbpost.objects.all()
    valid_posts = []
    for post in posts:
        for keyword in keywords:
            if keyword in comment['message']:
                valid_posts.append(post)
                break
    return HttpResponse({
        'fb_comments': valid_comments[:100],
        'fb_comments_count': len(valid_comments),
        'fb_posts': valid_posts[:100],
        'fb_posts_count': len(valid_posts)
        }, safe=False)

def insert_fbpost(content, pagename, timestamp):
    Fbpost.objects.create(
        content=content,
        pagename=pagename,
        timestamp=timestamp
    )
    print('.', end='', file=sys.stderr)


def insert_fbcomment(message, username, timestamp):
    try:
        Fbcomment.objects.create(
            message=message,
            username=username,
            timestamp=timestamp
        )
    except:
        # print('active_threads:%d', threading.active_count())  # temporary
        time.sleep(2)
    print('.', end='', file=sys.stderr)



def save_scraped_objects_to_db():
    print("checking facebook for posts and comments...")
    store = scrape_facebook()
    comments = store['post_comments_list']
    posts = store['post_content_list']
    print("found %d posts and %d comments for inserting into db" % (len(posts), len(comments)), file=sys.stderr)
    print("inserting posts to db ", end='', file=sys.stderr)
    for i, post in enumerate(posts):
        if (i%500 == 0): print("Posts inserted: %d" % i)
        while threading.active_count() > 100:
            time.sleep(1)
        if Fbpost.objects.filter(timestamp=post['timestamp'], content=post['content']):
            print('!', end='', file=sys.stderr)
            continue
        if not post['content']:
            print('-', end='', file=sys.stderr)
            continue
        threading.Thread(target=insert_fbpost, kwargs={
            'content': post['content'],
            'pagename': post['page_name'],
            'timestamp': post['timestamp']
            }).start()
    print('\ninserting comments to db', end='', file=sys.stderr)
    for i, comment in enumerate(comments):
        if(i % 1000 == 0): print("Comments inserted: %d" % i)
        while threading.active_count() > 100:
            time.sleep(1)
        if Fbcomment.objects.filter(timestamp=comment['timestamp'], message=comment['message']):
            print('!', end='', file=sys.stderr)
            continue
        if not comment['message']:
            print('-', end='', file=sys.stderr)
            continue
        threading.Thread(target=insert_fbcomment, kwargs={
            'message': comment['message'],
            'username': comment['user'],
            'timestamp': comment['timestamp']
            }).start()
    print('done with the db!!!', file=sys.stderr)

