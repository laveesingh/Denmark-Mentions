# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import threading
import time
import os
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from facebook_script import scrape_facebook
from youtube_script import scrape_youtube

from app.models import Ytcomment, Fbpost, Fbcomment, ObjectHash


def update(request):
    data = request.POST
    access_token = data.get('access_token')
    if not access_token:
        return JsonResponse({
            'msg': 'access token not supplied'
        })
    print('database update requested')
    print('starting youtube thread')
    threading.Thread(
        target=scrape_youtube
    ).start()
    print('starting facebook thread')
    threading.Thread(
        target=scrape_facebook,
        kwargs={
            'access_token': access_token
        }
    ).start()
    # scrape_facebook(access_token)
    # scrape_youtube()
    return JsonResponse({'msg': 'update in progress'})

