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
        for keyword in keywords:
            if keyword in comment.message:
                valid_comments.append(comment)
                break
    posts = Fbpost.objects.all()
    valid_posts = []
    for post in posts:
        for keyword in keywords:
            if keyword in post.content:
                valid_posts.append(post)
                break
    return {
        'fb_comments': valid_comments[:100],
        'fb_comments_count': len(valid_comments),
        'fb_posts': valid_posts[:100],
        'fb_posts_count': len(valid_posts)
        }
