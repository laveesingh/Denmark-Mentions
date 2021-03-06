# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import threading
import time
import os
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from scripts.facebook_script import scrape_facebook
from scripts.youtube_script import scrape_youtube
from scripts.twitter_script import scrape_twitter
from app.update_json import handle_user_update


def update(request):
    data = request.GET
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
    print('starting twitter thread')
    threading.Thread(
        target=scrape_twitter
    ).start()
    return JsonResponse({'msg': 'update in progress'})


def user_list_update(request):
    data = request.GET
    user_list = data.get('user_list').split()
    handle_user_update(user_list)
    return JsonResponse({'msg': 'successfully updated the list'})
