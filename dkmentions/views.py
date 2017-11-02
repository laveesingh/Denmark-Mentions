# -*- coding: utf-8 -*-

from django.shortcuts import render

from app.forms import Form
from app.models import Fbcomment, Fbpost, Ytcomment


def main(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data.get('keywords')
            results = search(keywords)
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

    fb_comments = Fbcomment.objects.all()
    valid_fb_comments = []
    for comment in fb_comments:
        occ = 0
        word_set = set(s.lower() for s in comment.message.split())
        for keyword in keywords:
            if keyword.lower() in word_set:
                occ += 1
        if occ > 0:
            valid_fb_comments.append((occ, comment))

    fb_posts = Fbpost.objects.all()
    valid_fb_posts = []
    for post in fb_posts:
        occ = 0
        word_set = set(s.lower() for s in post.content.split())
        for keyword in keywords:
            if keyword.lower() in word_set:
                occ += 1
                # valid_fb_posts.append(post)
                # break
        if occ > 0:
            valid_fb_posts.append((occ, post))

    yt_comments = Ytcomment.objects.all()
    valid_yt_comments = []
    for comment in yt_comments:
        occ = 0
        word_set = set(s.lower() for s in comment.message.split())
        for keyword in keywords:
            if keyword.lower() in word_set:
                occ += 1
        if occ > 0:
            valid_yt_comments.append((occ, comment))

    valid_fb_comments.sort(key=lambda comment: comment[0])
    valid_fb_posts.sort(key=lambda post: post[0])
    valid_yt_comments.sort(key=lambda comment: comment[0])
    valid_fb_comments = [y for x, y in valid_fb_comments]
    valid_fb_posts = [y for x, y in valid_fb_posts]
    valid_yt_comments = [y for x, y in valid_yt_comments]

    return {
        'fb_comments': valid_fb_comments[:100],
        'fb_comments_count': len(valid_fb_comments),
        'fb_posts': valid_fb_posts[:100],
        'fb_posts_count': len(valid_fb_posts),
        'yt_comments': valid_yt_comments[:100],
        'yt_comments_count': len(valid_yt_comments)
    }
