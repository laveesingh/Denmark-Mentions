# -*- coding: utf-8 -*-

from collections import defaultdict
from operator import and_, or_
import time
import datetime
import xlwt
import re

from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse

from app.forms import Form
from app.models import Fbcomment, Fbpost, Ytcomment, Tweet
from app.utils import export_to_excel
from app.utils import sort_by_key_occ
from app.utils import highlight_occurrences
from app.utils import extract_search_elements
from app.utils import validate_timestamp
from app.utils import fetch_filters


def main(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data.get('keywords')
            timestamp = form.cleaned_data.get('date')
            export = form.cleaned_data.get('export_to_excel')
            # ids = form.cleaned_data.get('ids').split()
            # results = search(keywords, timestamp, ids)
            results = search(keywords, timestamp)
            # inject html to highlight occurrences
            highlight_occurrences(' '.join(extract_search_elements(keywords)[0]), results)
        else:
            results = defaultdict(int)
            keywords = "ERROR!!!"
        context = dict(results)
        context['form'] = form
        if export:
            return export_to_excel(keywords, context)
        # print('context:', context)
        return render(request, 'template.html', context)
    form = Form()
    return render(request, 'template.html', {
        'form': form
    })

def search(qstring, timestamp):
    if timestamp:
        timestamp = validate_timestamp(timestamp)
    keywords, usernames, userids = extract_search_elements(qstring)
    # keywords_filter, fbc_user_filter, fbp_user_filter, ytc_user_filter,\
            # tweet_user_filter = fetch_filters(keywords, usernames, userids, timestamp)

    # valid_fb_posts = Fbpost.objects.filter(keywords_filter & fbp_user_filter)
    # valid_fb_comments = Fbcomment.objects.filter(keywords_filter & fbc_user_filter)
    # valid_yt_comments = Ytcomment.objects.filter(keywords_filter & ytc_user_filter)
    # valid_tweets = Tweet.objects.filter(keywords_filter & tweet_user_filter)
    print "keywords:", keywords
    print "userids: ", userids
    print 'usernames:', usernames
    try: 
        keyword_filter = reduce(or_, [Q(message__icontains=keyword) for keyword in keywords])
    except: 
        keyword_filter = Q()
    try: 
        user_filter = reduce(or_, [Q(user_id__iregex=r'%s'%userid) for userid in userids] +\
                [Q(username__iregex=r'%s'%username.lower()) for username in usernames])
    except:
        user_filter = Q()

    valid_fb_posts = Fbpost.objects.filter(keyword_filter, user_filter)
    valid_fb_comments = Fbcomment.objects.filter(keyword_filter, user_filter)
    valid_yt_comments = Ytcomment.objects.filter(keyword_filter, user_filter)
    valid_tweets = Tweet.objects.filter(keyword_filter, user_filter)

    valid_fb_posts = list(valid_fb_posts)
    valid_fb_comments = list(valid_fb_comments)
    valid_yt_comments = list(valid_yt_comments)
    valid_tweets = list(valid_tweets)

    sort_by_key_occ(valid_fb_posts, keywords)
    sort_by_key_occ(valid_fb_comments, keywords)
    sort_by_key_occ(valid_yt_comments, keywords)
    sort_by_key_occ(valid_tweets, keywords)
    return {
        'fb_comments': valid_fb_comments,
        'fb_comments_count': len(valid_fb_comments),
        'fb_posts': valid_fb_posts,
        'fb_posts_count': len(valid_fb_posts),
        'yt_comments': valid_yt_comments,
        'yt_comments_count': len(valid_yt_comments),
        'tweets': valid_tweets,
        'tweets_count': len(valid_tweets)
    }


