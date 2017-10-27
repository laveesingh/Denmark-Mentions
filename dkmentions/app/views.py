# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from django.shortcuts import render

from facebook_script import scrape_facebook
from app.models import Ytcomment, Fbpost, Fbcomment, ObjectHash

def obj_hash(obj):
    # hash_str = ''.join(sorted(str(s) for s in obj.values()))
    hash_str = []
    for s in obj.values():
        try:
            for char in s:
                try:
                    hash_str.append(char)
                except:
                    pass
        except:
            pass
    hash_str = ''.join(hash_str)
    return hash(hash_str)

def update(request):
    save_scraped_objects_to_db()


def save_scraped_objects_to_db():
    f = open("logs.log", 'w', 0)
    print("scraping facebook", file=f)
    store = scrape_facebook()
    print("done scraping facebook", file=f)
    print("store is ", store.keys(), file=f)
    comments = store['post_comments_list']
    posts = store['post_content_list']
    hashes = ObjectHash.objects.all()
    hash_set = set()
    for _hash in hashes: hash_set.add(_hash)
    print("%d posts and %d comments" % (len(posts), len(comments)), file=f)
    for post in posts:
        post_hash = obj_hash(post)
        if post_hash in hash_set:
            print("found fb post in hash set", file=f)
            continue
        try:
            Fbpost.objects.create(
                    content=post['content'],
                    pagename=post['page_name'],
                    timestamp=post['timestamp'],
                    )
            print("successfully inserted fb post", file=f)
        except Exception as e:
            print("error occurred: ", e, file=f)
        ObjectHash.objects.create(hash_value=post_hash)
    for comment in comments:
        comment_hash = obj_hash(comment)
        if comment_hash in hash_set:
            print("found fb comment in hash set", file=f)
            continue
        try:
            Fbcomment.objects.create(
                    message=comment['message'],
                    username=comment['user'],
                    timestamp=comment['timestamp'],
                    )
            print("successfully inserted fb comment", file=f)
        except Exception as e:
            print("error occurred: ", e, file=f)
        ObjectHash.objects.create(hash_value=comment_hash)

# save_scraped_objects_to_db()
