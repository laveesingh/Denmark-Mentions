# -*- coding: utf-8 -*-

from collections import defaultdict
import time
import datetime

from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone

from app.forms import Form
from app.models import Fbcomment, Fbpost, Ytcomment


def main(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data.get('keywords')
            timestamp = form.cleaned_data.get('date')
            results = search(keywords, timestamp)

        else:
            results = defaultdict(int)
        context = {
            'form': form,
            'fb_comments': results['fb_comments'],
            'fb_comments_count': results['fb_comments_count'],
            'fb_posts': results['fb_posts'],
            'fb_posts_count': results['fb_posts_count'],
            'yt_comments': results['yt_comments'],
            'yt_comments_count': results['yt_comments_count']
        }
        # print('context:', context)
        return render(request, 'template.html', context)
    form = Form()
    return render(request, 'template.html', {
        'form': form
    })

def search(keywords, timestamp):
    keywords = keywords.split()
    if timestamp:
        time_tuple = datetime.datetime.strptime(timestamp, '%d-%m-%Y').timetuple()
        timestamp = time.mktime(time_tuple)
        timestamp = datetime.datetime.fromtimestamp(timestamp)
        timestamp = timezone.make_aware(timestamp)
        print "timestamp:", timestamp
    qset = Q()
    for keyword in keywords:
        qset |= Q(message__icontains=keyword)
    if timestamp:
        nqset = qset & Q(timestamp__gt=timestamp)
    else:
        nqset = qset
    valid_fb_posts = Fbpost.objects.filter(nqset)
    valid_fb_comments = Fbcomment.objects.filter(nqset)
    valid_yt_comments = Ytcomment.objects.filter(nqset)
    return {
        'fb_comments': valid_fb_comments,
        'fb_comments_count': len(valid_fb_comments),
        'fb_posts': valid_fb_posts,
        'fb_posts_count': len(valid_fb_posts),
        'yt_comments': valid_yt_comments,
        'yt_comments_count': len(valid_yt_comments)
    }
