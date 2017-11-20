# -*- coding: utf-8 -*-

from __future__ import print_function
import requests
import json
import sys
import os
import threading
import time
import datetime
import random

from yt_channels_list import dump_to_file

from app.models import Ytcomment

api_key = "AIzaSyBBrX78q8Q9VP1BxZEWr0s7Xa7vWI8yA8A"
base_url = "https://www.googleapis.com/youtube/v3"
videos_url_format = '%s/playlistItems?%sorder=date&part=%s&playlistId=%s&maxResults=%s&key=%s'
channel_url_format = '%s/channels?id=%s&key=%s&part=%s'
comments_url_format = '%s/commentThreads?%svideoId=%s&maxResults=%s&key=%s&part=%s'

channels_object = {}
finished_channels = 0

f = open('youtube.log', 'w', 0)

def log(s):
    print(s, file=f)

def inline_log(s):
    print(s, end=' ', file=f)


def scrape_youtube():
    log('youtube scraping started: %s' % datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))
    channel_ids = json.loads(open('archive/yt_channels_list.json', 'r').read()).get('yt_channels_list')
    random.shuffle(channel_ids)
    for channel_id in channel_ids:
        part = 'snippet,contentDetails'
        channel_url = channel_url_format % (base_url, channel_id, api_key, part)
        channel_object = json.loads(requests.get(channel_url).content)
        if channel_object.get('items') is None or len(channel_object.get('items')) < 1:
            inline_log('?')
            continue
        try:
            playlist_id = channel_object['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        except:
            inline_log('?')
            continue
        next_page = ''
        for _iteration in xrange(20):
            inline_log('_')
            videos_url = videos_url_format % (base_url, next_page, part, playlist_id, str(50), api_key)
            video_objects_dict = json.loads(requests.get(videos_url).content)
            video_object_list = video_objects_dict.get('items')
            random.shuffle(video_object_list)
            print("%d videos found" % len(video_object_list))
            if not video_object_list: continue
            for video_object in video_object_list:
                video_id = video_object.get('contentDetails').get('videoId')
                video_name = video_object.get('snippet').get('title')
                next_page_token = ''
                cpart = 'snippet,replies'
                for __iteration in xrange(100):
                    comments_url = comments_url_format %  (base_url, next_page_token, video_id, str(100), api_key, cpart)
                    comment_objects_dict = json.loads(requests.get(comments_url).content)
                    comment_object_list = comment_objects_dict.get('items')
                    if not comment_object_list: 
                        inline_log('---')
                        break
                    for comment_object in comment_object_list:
                        comment_id = comment_object.get('id')
                        snippet = comment_object.get('snippet').get('topLevelComment').get('snippet')
                        username = snippet.get('authorDisplayName')
                        message = snippet.get('textDisplay')
                        timestamp = snippet.get('publishedAt')
                        query_set = Ytcomment.objects.filter(timestamp=timestamp, message=message)
                        if query_set:
                            try:
                                instance = query_set.first()
                                instance.channel_id = channel_id
                                instance.video_id = video_id
                                instance.comment_id = comment_id
                                instance.save()
                                inline_log('-+')
                            except:
                                inline_log('-?')
                            continue
                        try:
                            Ytcomment.objects.create(
                                channel_id=channel_id,
                                video_id=video_id,
                                comment_id=comment_id,
                                username=username,
                                message=message,
                                timestamp=timestamp,
                                video=video_name
                            )
                            inline_log('++')
                        except:
                            inline_log('+?')

                        
                        if comment_object.get('replies') is None:
                            continue
                        for comment in comment_object.get('replies').get('comments'):
                            timestamp = comment.get('snippet').get('publishedAt')
                            message = comment.get('snippet').get('textDisplay')
                            comment_id = comment.get('id')
                            query_set = Ytcomment.objects.filter(timestamp=timestamp, message=message)
                            if query_set:
                                try:
                                    instance = query_set.first()
                                    instance.channel_id = channel_id
                                    instance.video_id = video_id
                                    instance.comment_id = comment_id
                                    instance.save()
                                    inline_log('-+')
                                except:
                                    inline_log('-?')
                                continue
                            try:
                                Ytcomment.objects.create(
                                        channel_id=channel_id,
                                        video_id=video_id,
                                        comment_id=comment_id,
                                        username=username,
                                        message=message,
                                        timestamp=timestamp,
                                        video=video_name
                                        )
                                inline_log('++')
                            except:
                                inline_log('+?')


                    if 'nextPageToken' in comment_objects_dict:
                        next_page_token = 'pageToken=%s&' % comment_objects_dict.get('nextPageToken')
                    else:
                        break
            if video_objects_dict.get('nextPageToken'):
                next_page = 'pageToken=%s&' % video_objects_dict.get('nextPageToken')
            else:
                break
