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
        form.is_valid()
        keywords = form.cleaned_data.get('keywords')
        users = form.cleaned_data.get('users')
        if not keywords and not users:
            return HttpResponse(
                    '''No input field specified!!! <a href='/'>Go Back</a>'''
                    )
        keywords, users = extract_search_elements(keywords if keywords else '', users if users else '')
        if not keywords and not users:
            return HttpResponse(
                    '''Something wrong with input!!! <a href='/'>Go Back</a>'''
                    )
        timestamp = form.cleaned_data.get('date')
        export = form.cleaned_data.get('export_to_excel')
        results = search(keywords, users, timestamp)
        if not export:
            highlight_occurrences(' '.join(keywords), results)
        context = dict(results)
        context['form'] = form
        if export:
            return export_to_excel(keywords, context)
        return render(request, 'template.html', context)
    form = Form()
    return render(request, 'template.html', {
        'form': form
    })

def search(keywords, users, timestamp):
    if timestamp:
        timestamp = validate_timestamp(timestamp)
        time_filter = Q(timestamp__gt=timestamp)
    else:
        time_filter = Q()
    try: 
        tempkeywords = [word for keyword in keywords for word in keyword.split('+')]
        keyword_filter = reduce(or_, [Q(message__icontains=keyword) for keyword in tempkeywords])
        and_filter = Q()
        for keyword in keywords:
            temp_filter = Q()
            for word in keyword.split('+'):
                temp_filter &= Q(message__icontains=word.strip())
            and_filter |= temp_filter
    except: 
        print 'error occurred during creation of keyword filter'
        keyword_filter = Q()
    try: 
        user_filter = reduce(or_, [Q(user_id__iregex=r'%s'%user.strip()) for user in users] +\
                [Q(username__iregex=r'%s'%user.strip()) for user in users])
        print 'error occurred during creation of user filter'
    except:
        user_filter = Q()

    valid_fb_posts = list(Fbpost.objects.filter(and_filter).filter(user_filter).filter(time_filter))
    valid_fb_comments = list(Fbcomment.objects.filter(and_filter).filter(user_filter).filter(time_filter))
    valid_yt_comments = list(Ytcomment.objects.filter(and_filter).filter(user_filter).filter(time_filter))
    valid_tweets = list(Tweet.objects.filter(and_filter).filter(user_filter).filter(time_filter))

    sort_by_key_occ(valid_fb_posts, keywords)
    sort_by_key_occ(valid_fb_comments, keywords)
    sort_by_key_occ(valid_yt_comments, keywords)
    sort_by_key_occ(valid_tweets, keywords)
    return {
        'fb_comments': valid_fb_comments, 'fb_comments_count': len(valid_fb_comments),
        'fb_posts': valid_fb_posts, 'fb_posts_count': len(valid_fb_posts),
        'yt_comments': valid_yt_comments, 'yt_comments_count': len(valid_yt_comments),
        'tweets': valid_tweets, 'tweets_count': len(valid_tweets)
    }

