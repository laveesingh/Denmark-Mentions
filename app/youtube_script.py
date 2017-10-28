from __future__ import print_function
import requests
import json
import sys
import os
import threading
import time

from yt_channels_list import dump_to_file

api_key = "AIzaSyBBrX78q8Q9VP1BxZEWr0s7Xa7vWI8yA8A"
base_url = "https://www.googleapis.com/youtube/v3"

channel_objects = []
finished_channels = 0
def log(s):
	print(s, file=sys.stderr)

def fetch_channel_obj(channel_id, channel_no):
	global finished_channels
	log('fetching channel no: %d' % channel_no)
	part = "snippet,contentDetails"
	url = base_url + "/channels?id=" + channel_id + "&key=" + api_key + "&part=" + part
	response = requests.get(url)
	rjson = json.loads(response.content)
	if 'error' in rjson:
		log('finished_channels: %d' % finished_channels)
		return
	if len(rjson["items"]) == 0:
		log('finished_channels: %d' % finished_channels)
		return
	try:
		playlist_id = rjson["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
	except:
		print("rjson:", rjson)
		sys.exit(1)
	channel_objects.append({
		'channel_name': rjson["items"][0]["snippet"]['title'],
		'playlist_id': playlist_id,
		'videos': fetch_videos_list(playlist_id, channel_no)
	})
	finished_channels += 1
	log('finished_channels: %d' % finished_channels)


def fetch_videos_list(playlist_id, channel_no):
	videos_objects = []
	part = "snippet,contentDetails"
	next_page = ""
	while True:
		log("Stuck in while videos")
		url = base_url + "/playlistItems?"+next_page+"order=date&part=" + part + "&playlistId=" + playlist_id + \
			"&maxResults=10&key=" + api_key
		log("fetching videos for channel_no %d"%channel_no)
		response = requests.get(url)
		rjson = json.loads(response.content)
		if('error' in rjson):
			break
		for item in rjson.get('items'):
			video_id = item["contentDetails"]["videoId"]
			videos_objects.append({
				'title': item["snippet"]["title"],
				'video_id': video_id,
				'comments': fetch_comments_list(video_id, channel_no)
			})
		if("nextPageToken" in rjson):
			next_page="pageToken=" + rjson["nextPageToken"] + "&"
		else:
			break
		if len(videos_objects) >= 10:  # Temporary
			break
	return videos_objects


def fetch_comments_list(video_id, channel_no):
	part = "snippet,replies"
	next_page = ""
	comments_objects = []
	while True:
		log("stuck in while comments")
		url = base_url + "/commentThreads?" + next_page + "videoId=" + video_id + "&maxResults=100&key=" + api_key + "&part=" + part
		log("Fetching comment for channel: %d, video: %s" % (channel_no, video_id))
		response = requests.get(url)
		rjson = json.loads(response.content)
		if('error' in rjson):
			break
		for item in rjson['items']:
			comments_objects.append({
				'user': item["snippet"]["topLevelComment"]['snippet']['authorDisplayName'],
				'message': item["snippet"]["topLevelComment"]['snippet']['textDisplay'],
				'timestamp': item["snippet"]["topLevelComment"]['snippet']['publishedAt'],
				})
			replycount = item["snippet"]["totalReplyCount"]
			if(replycount > 0):
				if('replies' in item):
					for com in item["replies"]["comments"]:
						comment={}
						comment["user"] = com["snippet"]["authorDisplayName"]
						comment["message"] = com["snippet"]["textDisplay"]
						comment["timestamp"] = com["snippet"]["publishedAt"]
						comments_objects.append(comment)
		if("nextPageToken" in rjson):
			next_page="pageToken=" + rjson["nextPageToken"] + "&"
		else:
			break
		if len(comments_objects) >= 40:  # Temporary
			break

	return comments_objects

def load_channel_list():
	if os.path.isfile("yt_channels_list.json"):
		log("found json for pages list!")
	else:
		dump_to_file()
	json_data = open("yt_channels_list.json", 'r').read()
	store = json.loads(json_data)
	return store["yt_channels_list"]

def scrape_youtube():
	channel_no = 0
	channel_ids = load_channel_list()
	channel_ids = channel_ids[:11] # temporary
	for channel_id in channel_ids:
		while threading.active_count() > 100:
			log("sleeping for some rest")
			time.sleep(10)
		threading.Thread(target=fetch_channel_obj, kwargs=({'channel_id': channel_id, 'channel_no': channel_no})).start()
		channel_no += 1
		log('channel_no: %d, finished_channels: %d' % (channel_no, finished_channels))

	while threading.active_count() > 4:
		log("active threads: %d" % threading.active_count())
		time.sleep(10)

	return channel_objects