import json
import requests
import re

def update_facebook_json(users_list):
    f = open('archive/fb_pages_list.json', 'r')
    json_data = json.load(f)
    existing_list = json_data.get('fb_pages_list')
    for user in users_list:
        if user not in existing_list:
            print 'appending', user, 'into facebook'
            existing_list.append(user)
    json_data['fb_pages_list'] = existing_list
    f = open('archive/fb_pages_list.json', 'w')
    json.dump(json_data, f)

def update_youtube_json(users_list):
    f = open('archive/yt_channels_list.json', 'r')
    json_data = json.load(f)
    existing_list = json_data.get('yt_channels_list')
    for user in users_list:
        if user not in existing_list:
            existing_list.append(user)
            print 'appending', user, 'into youtube'
    json_data['yt_channels_list'] = existing_list
    f = open('archive/yt_channels_list.json', 'w')
    json.dump(json_data, f)


def facebook_get_id_from_url(url):
    response = requests.get(url)
    user_id = re.findall(r'fb://page/(\d+)', response.content)
    if not user_id: return '239755226144854'
    return user_id[0]

def handle_user_update(user_list):
    facebook_list = []
    youtube_list = []
    for i in xrange(len(user_list)):
        if 'facebook.com' in user_list[i]:
            user_list[i] = facebook_get_id_from_url(user_list[i])
            facebook_list.append(user_list[i])
        if 'youtube.com' in user_list[i]:
            match = re.search(user_list[i], 'youtube.com/(user|channel)/(?P<hash>\w+)')
            if match:
                user_list[i] = match.group('hash')
                youtube_list.append(user_list[i])
            else:
                user_list[i] = ''
    update_facebook_json(facebook_list)
    update_youtube_json(youtube_list)
