# -*- coding: utf-8 -*-

from collections import defaultdict

from django.shortcuts import render
from django.db.models import Q

from app.forms import Form
from app.models import Fbcomment, Fbpost, Ytcomment


def main(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data.get('keywords')
            results = search(keywords)
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

def search(keywords):
    keywords = keywords.split()
    qset = Q()
    for keyword in keywords:
        qset |= Q(message__icontains=keyword)
    valid_fb_posts = Fbpost.objects.filter(qset)
    valid_fb_comments = Fbcomment.objects.filter(qset)
    valid_yt_comments = Ytcomment.objects.filter(qset)
    return {
        'fb_comments': valid_fb_comments,
        'fb_comments_count': len(valid_fb_comments),
        'fb_posts': valid_fb_posts,
        'fb_posts_count': len(valid_fb_posts),
        'yt_comments': valid_yt_comments,
        'yt_comments_count': len(valid_yt_comments)
    }
