from django.shortcuts import render

from app.forms import Form
from app.models import Fbcomment, Fbpost


def main(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data.get('keywords')
            results = search(keywords)
        return render(request, 'template.html', {
            'form': form,
            'fb_comments': results['fb_comments'],
            'fb_comments_count': results['fb_comments_count'],
            'fb_posts': results['fb_posts'],
            'fb_posts_count': results['fb_posts_count'],
        })
    form = Form()
    return render(request, 'template.html', {
        'form': form
    })

def search(keywords):
    keywords = keywords.split()
    comments = Fbcomment.objects.all()
    valid_comments = []
    for comment in comments:
        word_set = set(s.lower() for s in comment.message.split())
        for keyword in keywords:
            if keyword.lower() in word_set:
                valid_comments.append(comment)
                break
    posts = Fbpost.objects.all()
    valid_posts = []
    for post in posts:
        word_set = set(s.lower() for s in post.content.split())
        for keyword in keywords:
            if keyword.lower() in word_set:
                valid_posts.append(post)
                break
    return {
        'fb_comments': valid_comments[:100],
        'fb_comments_count': len(valid_comments),
        'fb_posts': valid_posts[:100],
        'fb_posts_count': len(valid_posts)
        }
