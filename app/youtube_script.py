from __future__ import print_function
import requests
import json
import sys
import os
import threading
import time
import datetime

from yt_channels_list import dump_to_file

from app.models import Ytcomment

api_key = "AIzaSyBBrX78q8Q9VP1BxZEWr0s7Xa7vWI8yA8A"
base_url = "https://www.googleapis.com/youtube/v3"
videos_url_format = '%s/playlistItems?%sorder=date&part=%s&playlistId=%s&maxResults=%s&key=%s'
channel_url_format = '%s/channels?id=%s&key=%s&part=%s'
comments_url_format = '%s/commentThreads?%svideoId=%s&maxResults=%s&key=%s&part=%s'

channels_object = {}
finished_channels = 0

f = open('yt_logs.log', 'w', 0)

def log(s):
    # print(s, file=sys.stderr)
    print(s, file=f)

def inline_log(s):
    # print(s, end=' ', file=sys.stderr)
    print(s, end=' ', file=f)


def scrape_youtube():
    log('youtube started: %s' % datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))
    print('youtube started: %s' % datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))
    channel_ids = load_channel_list()
    channel_ids = channel_ids # temporary
    for channel_id in channel_ids:
        time.sleep(5)
        while threading.active_count() > 100: # temporary
            time.sleep(5)
        threading.Thread(
            target=fetch_channel_obj, 
            kwargs={
                'channel_id': channel_id
            }
        ).start()
        # fetch_channel_obj(channel_id)


def fetch_channel_obj(channel_id):
    inline_log('^ch')
    part = "snippet,contentDetails"
    channel_url = channel_url_format % (base_url, channel_id, api_key, part)
    response = requests.get(channel_url)
    rjson = json.loads(response.content)
    if rjson.get('items') is None or len(rjson.get('items')) < 1:
        time.sleep(.2)
        rjson = json.loads(requests.get(channel_url).content)
        if rjson.get('items') is None or len(rjson.get('items')) < 1:
            inline_log('?channel_err')
            return
    try:
        playlist_id = rjson["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    except Exception as e:
        inline_log(rjson)
        return

    channels_object[channel_id] = {
        'channel_name': rjson['items'][0]['snippet']['title'],
        'playlist_id': playlist_id,
        'videos': {}
    }
    if threading.active_count() > 50: time.sleep(2)
    threading.Thread(
        target=fetch_videos_list,
        kwargs={
            'playlist_id': playlist_id,
            'videos_object': channels_object[channel_id]['videos']
        }
    ).start()

def fetch_videos_list(playlist_id, videos_object):
    inline_log('^v')
    part = "snippet,contentDetails"
    next_page = ""
    while True:
        videos_url = videos_url_format % (base_url, next_page, part, playlist_id, str(10), api_key)
        response = requests.get(videos_url)
        rjson = json.loads(response.content)
        if rjson.get('items') is None:
            break
        for item in rjson.get('items'):
            if threading.active_count() > 50: time.sleep(2)
            video_id = item["contentDetails"]["videoId"]
            videos_object[video_id] = {
                'title': item['snippet']['title'],
                'video_id': video_id,
                'comments': {}
            }
            inline_log('?c')
            threading.Thread(
                target=fetch_comments_list,
                kwargs={
                    'video_id': video_id,
                    'comments_object': videos_object[video_id]['comments'],
                    'video_title': item['snippet']['title']
                }
            ).start()
            if len(videos_object.keys()) > 2: # temporary
                break
        if len(videos_object.keys()) > 2: # temporary
            break
        if rjson.get('nextPageToken'):
            next_page="pageToken=" + rjson["nextPageToken"] + "&"
        else:
            break


def fetch_comments_list(video_id, video_title, comments_object):
    inline_log('.c')
    part = "snippet,replies"
    next_page = ""
    while True:
        comments_url = comments_url_format % (base_url, next_page, video_id, str(100), api_key, part)
        response = requests.get(comments_url)
        rjson = json.loads(response.content)
        if rjson.get('items') is None:
            break
        for item in rjson['items']:
            if threading.active_count() > 50: time.sleep(2)
            snippet = item["snippet"]["topLevelComment"]['snippet']
            comments_object[item['id']] = {
                'user': snippet['authorDisplayName'],
                'message': snippet['textDisplay'],
                'timestamp': snippet['publishedAt']
            }
            # inserting to database
            inline_log('>') # to db
            if Ytcomment.objects.filter(timestamp=snippet['publishedAt'], message=snippet['textDisplay']):
                inline_log('^')
                continue
            try:
                if Ytcomment.objects.filter(timestamp=snippet['publishedAt'], message=snippet['textDisplay']):
                    continue
                Ytcomment.objects.create(
                    username=snippet['authorDisplayName'],
                    message=snippet['textDisplay'],
                    timestamp=snippet['publishedAt'],
                    video = video_title,
                    channel = ''
                )
                inline_log('|')
            except Exception as e:
                log(e)
                inline_log('<')
            if item.get('replies') is None:
                continue
            for comment in item['replies']['comments']:
                if threading.active_count() > 50: time.sleep(2)
                comments_object[comment['id']] = {
                    'user': comment['snippet']['authorDisplayName'],
                    'message': comment['snippet']['textDisplay'],
                    'timestamp': comment['snippet']['publishedAt']
                }
                inline_log('>')
                try:
                    timestamp = comment['snippet']['publishedAt']
                    message = comment['snippet']['textDisplay']
                    if Ytcomment.objects.filter(timestamp=timestamp, message=message):
                        inline_log('^')
                        continue
                    Ytcomment.objects.create(
                        username = comment['snippet']['authorDisplayName'],
                        message = message,
                        timestamp = timestamp,
                        video = video_title,
                        channel = ''
                    )
                    inline_log('|') # okay
                except:
                    inline_log('<') # error inserting to db
        if("nextPageToken" in rjson):
            next_page="pageToken=" + rjson["nextPageToken"] + "&"
        else:
            break

def load_channel_list():
    if os.path.isfile("yt_channels_list.json"):
        log("found json for pages list!")
    else:
        dump_to_file()
    json_data = open("yt_channels_list.json", 'r').read()
    store = json.loads(json_data)
    return store["yt_channels_list"]

